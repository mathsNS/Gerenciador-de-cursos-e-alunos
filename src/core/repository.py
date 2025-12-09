import json
from pathlib import Path
from typing import Dict, Any

class Repository:
    def __init__(self, data_dir="data", mem=False):
        self.mem = mem

        self.cursos = {}
        self.alunos = {}
        self.turmas = {}
        self.matriculas = {}

        if not self.mem:
            self.base_path = Path(data_dir)
            self.base_path.mkdir(exist_ok=True)

            self._f_cursos = "cursos.json"
            self._f_alunos = "alunos.json"
            self._f_turmas = "turmas.json"
            self._f_matriculas = "matriculas.json"

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

    def add_turma(self, id_turma: str, codigo_curso: str, periodo: str, horarios: dict, vagas: int, local: str = None):
        from src.models.turma import Turma
        t = Turma(id_turma=id_turma, codigo_curso=codigo_curso, periodo=periodo, horarios=horarios, vagas=vagas, local=local)
        self.turmas[str(id_turma)] = t
        self.save_all()
        return t

    def get_turma(self, id_turma: str):
        return self.turmas.get(str(id_turma))

    def add_matricula(self, matricula_obj):
        # chave unica aluno_id
        aluno_id = getattr(matricula_obj.aluno, "matricula", matricula_obj.aluno)
        turma_id = getattr(matricula_obj.turma, "id_turma", matricula_obj.turma)
        chave = f"{aluno_id}_{turma_id}"
        self.matriculas[chave] = matricula_obj

        # adiciona na turma se existe
        turma = self.turmas.get(str(turma_id))
        if turma and hasattr(turma, "matriculas"):
            turma.matriculas.append(matricula_obj)
        self.save_all()
        return matricula_obj

    def get_matricula(self, aluno_id: str, turma_id: str):
        chave = f"{aluno_id}_{turma_id}"
        return self.matriculas.get(chave)

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
