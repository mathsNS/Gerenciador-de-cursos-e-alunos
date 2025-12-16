import json
from pathlib import Path
from src.models.turma import Turma
from src.models.horario import Horario

from typing import Dict, Any

class Repository:
    def __init__(self, data_dir="data", mem=False):
        self.mem = mem

        self.cursos = {}
        self.alunos = {}
        self.turmas = {}
        self.matriculas = {}

        self._f_cursos = "cursos.json"
        self._f_alunos = "alunos.json"
        self._f_turmas = "turmas.json"
        self._f_matriculas = "matriculas.json"

        if not self.mem:
            self.base_path = Path(data_dir)
            self.base_path.mkdir(exist_ok=True)
            self.load_all()

    def _write(self, filename, data):
        if self.mem:
            return
        path = self.base_path / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _read(self, filename):
        if self.mem:
            return {}
        path = self.base_path / filename
        if not path.exists():
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # def _write(self, filename: str, data):
    #     path = self.base_path / filename
    #     with open(path, "w", encoding="utf-8") as f:
    #         json.dump(data, f, ensure_ascii=False, indent=2)

    # def _read(self, filename: str):
    #     path = self.base_path / filename
    #     if not path.exists():
    #         return {}
    #     with open(path, "r", encoding="utf-8") as f:
    #         return json.load(f)

   # serialização
    def _serialize_aluno(self, aluno_obj):
        # aluno_obj instancia de Aluno
        historico = getattr(aluno_obj, "historico", None)
        if historico is None:
            historico = getattr(aluno_obj, "cursos_concluidos", [])
        
        # garante que historico é uma lista de dicts
        if isinstance(historico, str):
            historico = []
        elif not isinstance(historico, list):
            historico = []
        
        return {
            "matricula": aluno_obj.matricula,
            "nome": aluno_obj.nome,
            "email": getattr(aluno_obj, "email", None),
            "historico": historico
        }

    def _serialize_curso(self, curso_obj):
        return {
            "codigo": curso_obj.codigo,
            "nome": curso_obj.nome,
            "carga_horaria": curso_obj.carga_horaria,
            "prerequisitos": getattr(curso_obj, "prerequisitos", []),
            "ementa": getattr(curso_obj, "ementa", None)
        }

    def _serialize_turma(self, turma_obj):
        return {
            "id_turma": turma_obj.id_turma,
            "codigo_curso": turma_obj.codigo_curso,
            "periodo": turma_obj.periodo,
            "horarios": turma_obj.horarios,
            "vagas": turma_obj.vagas,
            "local": turma_obj.local,
            "aberta": getattr(turma_obj, "aberta", True)
        }

    def _serialize_matricula(self, chave, matricula_obj):
        aluno_id = getattr(matricula_obj.aluno, "matricula", matricula_obj.aluno)
        turma_id = getattr(matricula_obj.turma, "id_turma", matricula_obj.turma)
        estado = getattr(matricula_obj.estado, "value", str(getattr(matricula_obj, "estado", None)))
        return {
            "chave": chave,
            "aluno": aluno_id,
            "turma": turma_id,
            "nota": getattr(matricula_obj, "nota", None),
            "frequencia": getattr(matricula_obj, "frequencia", None),
            "estado": estado,
            "ativa": getattr(matricula_obj, "ativa", True)
        }

    def save_all(self):
        cursos_serial = {codigo: self._serialize_curso(obj) for codigo, obj in self.cursos.items()}
        self._write(self._f_cursos, cursos_serial)

        alunos_serial = {mat: self._serialize_aluno(obj) for mat, obj in self.alunos.items()}
        self._write(self._f_alunos, alunos_serial)

        turmas_serial = {tid: self._serialize_turma(obj) for tid, obj in self.turmas.items()}
        self._write(self._f_turmas, turmas_serial)

        # guarda a mnatricula como lista de obj simples
        matriculas_serial = {chave: self._serialize_matricula(chave, m) for chave, m in self.matriculas.items()}
        self._write(self._f_matriculas, matriculas_serial)

    def load_all(self):
        dados_cursos = self._read(self._f_cursos) or {}
        dados_alunos = self._read(self._f_alunos) or {}
        dados_turmas = self._read(self._f_turmas) or {}
        dados_matriculas = self._read(self._f_matriculas) or {}

        # import pra nao dar o problema de ciclo de novo
        from src.models.curso import Curso
        from src.models.aluno import Aluno
        from src.models.turma import Turma
        from src.models.matricula import Matricula, EstadoMatricula

        self.cursos = {}
        for codigo, c in dados_cursos.items():
            try:
                curso = Curso(
                    codigo=c.get("codigo", codigo),
                    nome=c.get("nome"),
                    carga_horaria=c.get("carga_horaria"),
                    prerequisitos=c.get("prerequisitos", []),
                    ementa=c.get("ementa")
                )
                self.cursos[codigo] = curso
            except Exception:
                # armazena o dict como raw caso nao consiga reconstruir
                self.cursos[codigo] = c

        self.alunos = {}
        for mat, a in dados_alunos.items():
            try:
                aluno = Aluno(matricula=a.get("matricula", mat), nome=a.get("nome"), email=a.get("email"))
                historico = a.get("historico", a.get("cursos_concluidos", []))
                
                # garabnte que historico nao é string
                if isinstance(historico, str):
                    historico = []
                elif not isinstance(historico, list):
                    historico = []
                else:
                    # depois valida
                    historico = [item if isinstance(item, dict) else {} for item in historico]
                
                # mantem os dois atributos
                setattr(aluno, "historico", historico)
                setattr(aluno, "cursos_concluidos", historico)
                self.alunos[mat] = aluno
            except Exception:
                self.alunos[mat] = a

        self.turmas = {}
        for tid, t in dados_turmas.items():
            try:
                turma = Turma(
                    id_turma=t.get("id_turma", tid),
                    codigo_curso=t.get("codigo_curso"),
                    periodo=t.get("periodo"),
                    horarios=t.get("horarios"),
                    vagas=t.get("vagas"),
                    local=t.get("local")
                )
                turma.aberta = t.get("aberta", True)
                turma.matriculas = []  
                self.turmas[tid] = turma
            except Exception:
                self.turmas[tid] = t

        # precisa ligar a alunos/turma
        self.matriculas = {}
        self.matriculas = {}
        for chave, m in (dados_matriculas or {}).items():
            try:
                aluno_id = m.get("aluno")
                turma_id = m.get("turma")
                aluno_obj = self.alunos.get(str(aluno_id))
                turma_obj = self.turmas.get(str(turma_id))

                matricula = Matricula(aluno=aluno_obj or aluno_id, turma=turma_obj or turma_id)
                matricula.nota = m.get("nota")
                matricula.frequencia = m.get("frequencia")
                estado_raw = m.get("estado")
                if estado_raw is not None:
                    try:
                        matricula.estado = EstadoMatricula(estado_raw)
                    except Exception:
                        # valor direto
                        matricula.estado = EstadoMatricula(matricula.estado.value)
                matricula.ativa = m.get("ativa", True)
                if isinstance(turma_obj, object) and hasattr(turma_obj, "matriculas"):
                    turma_obj.matriculas.append(matricula)

                self.matriculas[chave] = matricula
            except Exception:
                self.matriculas[chave] = m

    def add_curso(self, codigo: str, nome: str, carga_horaria: int, prerequisitos=None, ementa=None):
        from src.models.curso import Curso
        c = Curso(
            codigo=codigo,
            nome=nome,
            carga_horaria=carga_horaria,
            prerequisitos=prerequisitos,
            ementa=ementa
        )
        self.cursos[codigo] = c
        self.save_all()
        return c

    def get_curso(self, codigo: str):
        return self.cursos.get(codigo)

    def add_aluno(self, matricula: str, nome: str, email: str = None):
        from src.models.aluno import Aluno
        a = Aluno(matricula=matricula, nome=nome, email=email)
        if not hasattr(a, "historico"):
            setattr(a, "historico", getattr(a, "cursos_concluidos", []))
        self.alunos[str(matricula)] = a
        self.save_all()
        return a

    def get_aluno(self, matricula: str):
        return self.alunos.get(str(matricula))

    def add_turma(self, id_turma, codigo_curso, periodo, horarios: dict, vagas: int):
        if id_turma in self.turmas:
            raise ValueError("Turma já existe")

        horarios_obj = {dia: Horario(tempo) for dia, tempo in horarios.items()}
        turma = Turma(
            id_turma=id_turma,
            codigo_curso=codigo_curso,
            periodo=periodo,
            horarios=horarios_obj,
            vagas=vagas
        )

        self.turmas[id_turma] = turma
        self.save_all()
        return turma

    def get_turma(self, id_turma: str):
        return self.turmas.get(str(id_turma))

    def add_matricula(self, aluno_id: str, turma_id: str):
        # valida existência
        if aluno_id not in self.alunos:
            raise ValueError("Aluno inexistente")
        if turma_id not in self.turmas:
            raise ValueError("Turma inexistente")

        aluno = self.alunos[aluno_id]
        turma = self.turmas[turma_id]

        # 1) verifica pré-requisitos
        curso = self.cursos[turma.codigo_curso]
        for pre in curso.prerequisitos:
            if pre not in aluno.historico:
                raise ValueError("Aluno não cumpriu pré-requisitos")

        # 2) verifica choque de horário
        if hasattr(aluno, "matriculas"):
            for outra in aluno.matriculas:
                for h1 in turma.horarios.values():  # percorre os horários da turma que vai matricular
                    for h2 in outra.turma.horarios.values():  # percorre horários das turmas já matriculadas
                        if h1.choca_com(h2):
                            raise ValueError("Choque de horário")
        else:
            aluno.matriculas = []

        # 3) verifica vagas
        if hasattr(turma, "matriculas"):
            if len(turma.matriculas) >= turma.vagas:
                raise ValueError("Turma lotada")
        else:
            turma.matriculas = []

        # cria a matrícula
        from src.models.matricula import Matricula  # importe a classe Matricula
        matricula_obj = Matricula(aluno, turma)

        # adiciona na lista do repositório e do aluno/turma
        chave = f"{aluno_id}_{turma_id}"
        self.matriculas[chave] = matricula_obj
        aluno.matriculas.append(matricula_obj)
        turma.matriculas.append(matricula_obj)

        self.save_all()
        return matricula_obj

    def get_matricula(self, aluno_id: str, turma_id: str):
        chave = f"{aluno_id}_{turma_id}"
        return self.matriculas.get(chave)

    def lancar_nota(self, aluno, turma, nota):
        # normaliza ids recebidos (pode receber objeto ou id string)
        aluno_id = getattr(aluno, "matricula", aluno)
        turma_id = getattr(turma, "id_turma", turma)

        for chave, matricula in self.matriculas.items():
            # caso a matrícula esteja armazenada como dict (serializada)
            if isinstance(matricula, dict):
                m_aluno = matricula.get("aluno")
                m_turma = matricula.get("turma")
                if str(m_aluno) == str(aluno_id) and str(m_turma) == str(turma_id):
                    matricula["nota"] = nota
                    self.save_all()
                    return True, "Nota lançada com sucesso"

            # caso seja um objeto Matricula
            else:
                m_aluno = getattr(matricula.aluno, "matricula", matricula.aluno)
                m_turma = getattr(matricula.turma, "id_turma", matricula.turma)
                if str(m_aluno) == str(aluno_id) and str(m_turma) == str(turma_id):
                    matricula.nota = nota
                    self.save_all()
                    return True, "Nota lançada com sucesso"

        return False, "Matrícula não encontrada"

    def lancar_frequencia(self, aluno, turma, frequencia):
        # normaliza ids recebidos (pode receber objeto ou id string)
        aluno_id = getattr(aluno, "matricula", aluno)
        turma_id = getattr(turma, "id_turma", turma)

        for chave, matricula in self.matriculas.items():
            # caso a matrícula esteja armazenada como dict (serializada)
            if isinstance(matricula, dict):
                m_aluno = matricula.get("aluno")
                m_turma = matricula.get("turma")
                if str(m_aluno) == str(aluno_id) and str(m_turma) == str(turma_id):
                    matricula["frequencia"] = frequencia
                    self.save_all()
                    return True, "Frequência lançada com sucesso"

            # caso seja um objeto Matricula
            else:
                m_aluno = getattr(matricula.aluno, "matricula", matricula.aluno)
                m_turma = getattr(matricula.turma, "id_turma", matricula.turma)
                if str(m_aluno) == str(aluno_id) and str(m_turma) == str(turma_id):
                    matricula.frequencia = frequencia
                    self.save_all()
                    return True, "Frequência lançada com sucesso"

        return False, "Matrícula não encontrada"

    def concluir_matricula(self, aluno_id, turma_id):
        # move a matricula aprovada direto pro historico (para outros pre-requisitos)
        aluno_obj = self.alunos.get(str(aluno_id))
        turma_obj = self.turmas.get(str(turma_id))
        
        if aluno_obj is None or turma_obj is None:
            return False, "Aluno ou turma não encontrados"
        
        chave = f"{aluno_id}_{turma_id}"
        matricula = self.matriculas.get(chave)
        
        if matricula is None:
            return False, "Matrícula não encontrada"
        
        # dados da matricula
        if isinstance(matricula, dict):
            nota = matricula.get("nota")
            frequencia = matricula.get("frequencia")
        else:
            nota = getattr(matricula, "nota", None)
            frequencia = getattr(matricula, "frequencia", None)
        
        if nota is None or frequencia is None:
            return False, "Nota e frequência devem estar preenchidas"
        
        # Adiciona ao historico do aluno
        aluno_obj.adicionar_historico(
            curso=turma_obj.codigo_curso,
            nota=nota,
            frequencia=frequencia
        )
        
        # Remove matrícula ativa
        del self.matriculas[chave]
        self.save_all()
        
        return True, "Matrícula concluída e adicionada ao histórico"

    def alunos_por_turma(self, id_turma):
        if id_turma not in self.turmas:
            raise ValueError("Turma inexistente")

        turma = self.turmas[id_turma]
        alunos = [mat.aluno.matricula for mat in turma.matriculas] 

        return {
            "turma": id_turma,
            "total": len(alunos),
            "alunos": alunos
        }
    # def save_all(self):
    #     # wrapper (corrigir/revisar)
    #     self.save_alunos()
    #     self.save_cursos()
    #     self.save_turmas()
    #     self.save_matriculas()

    # def save_alunos(self):
    #     alunos_serial = {mat: self._serialize_aluno(obj) for mat, obj in self.alunos.items()}
    #     self._write(self._f_alunos, alunos_serial)

    # def save_cursos(self):
    #     cursos_serial = {codigo: self._serialize_curso(obj) for codigo, obj in self.cursos.items()}
    #     self._write(self._f_cursos, cursos_serial)

    # def save_turmas(self):
    #     turmas_serial = {tid: self._serialize_turma(obj) for tid, obj in self.turmas.items()}
    #     self._write(self._f_turmas, turmas_serial)

    # def save_matriculas(self):
    #     matriculas_serial = {chave: self._serialize_matricula(chave, m) for chave, m in self.matriculas.items()}
    #     self._write(self._f_matriculas, matriculas_serial)
