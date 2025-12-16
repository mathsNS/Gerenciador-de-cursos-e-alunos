import json
from src.core.repository import Repository
from src.models.matricula import Matricula
from datetime import datetime
from pathlib import Path
from src.models.matricula import Matricula, EstadoMatricula

SETTINGS_PATH = Path.cwd() / "settings.json"

def _load_settings():
    defaults = {
        "nota_minima_aprovacao": 6.0,
        "frequencia_minima": 75.0,
        "data_limite_trancamento": None,
        "max_turmas_por_aluno": None,
        "top_n_alunos": 10
    }
    if not SETTINGS_PATH.exists():
        return defaults
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            s = json.load(f)
        defaults.update(s or {})
    except Exception:
        pass
    return defaults

# dentro da classe Sistema:
class Sistema:
    def __init__(self):
        self.cursos = {}
        self.alunos = {}
        self.turmas = {}
        self.matriculas = {}
        self.settings = _load_settings()

    # encontra objeto Matricula por aluno+turma
    def _find_matricula(self, aluno_matricula, turma_id):
        for m in self.matriculas:
            if m.aluno_matricula == aluno_matricula and m.turma_id == turma_id:
                return m
        return None

    # Lançar nota (valida intervalo e atualiza)
    def lancar_nota(self, aluno_matricula: str, turma_id: str, nota: float):
        if nota is None:
            return False, "Nota não informada"
        if nota < 0 or nota > 10:
            return False, "Nota inválida (0-10)"
        m = self._find_matricula(aluno_matricula, turma_id)
        if not m:
            return False, "Matrícula não encontrada"
        m.nota = nota
        nota_min = float(self.settings.get("nota_minima_aprovacao", 6.0))
        freq_min = float(self.settings.get("frequencia_minima", 75.0))
        novo_estado = m.calcular_situacao(nota_min, freq_min)
        m.estado = novo_estado
        return True, f"Nota lançada. Situação: {m.estado.value}"

    # Lançar frequência (valida intervalo e atualiza)
    def lancar_frequencia(self, aluno_matricula: str, turma_id: str, frequencia: float):
        if frequencia is None:
            return False, "Frequência não informada"
        if frequencia < 0 or frequencia > 100:
            return False, "Frequência inválida (0-100)"
        m = self._find_matricula(aluno_matricula, turma_id)
        if not m:
            return False, "Matrícula não encontrada"
        m.frequencia = frequencia
        nota_min = float(self.settings.get("nota_minima_aprovacao", 6.0))
        freq_min = float(self.settings.get("frequencia_minima", 75.0))
        novo_estado = m.calcular_situacao(nota_min, freq_min)
        m.estado = novo_estado
        return True, f"Frequência lançada. Situação: {m.estado.value}"

    # Trancar matrícula até data limite
    def trancar_matricula(self, aluno_matricula: str, turma_id: str, referencia_data: datetime = None):
        m = self._find_matricula(aluno_matricula, turma_id)
        if not m:
            return False, "Matrícula não encontrada"

        data_lim_str = self.settings.get("data_limite_trancamento")
        if not data_lim_str:
            return False, "Trancamento não permitido (data limite não configurada)"
        try:
            data_lim = datetime.strptime(data_lim_str, "%Y-%m-%d").date()
        except Exception:
            return False, "Configuração de data_limite_trancamento inválida"

        hoje = (referencia_data or datetime.now()).date()
        if hoje > data_lim:
            return False, f"Prazo de trancamento expirado ({data_lim.isoformat()})"

        m.estado = EstadoMatricula.TRANCADO
        # se tiver atributo ativa, marca inativa
        if hasattr(m, "ativa"):
            m.ativa = False
        return True, "Matrícula trancada com sucesso"
    
class SistemaAcademico:
    def __init__(self):
        self.repo = Repository(mem=False)

    def lancar_nota(self, aluno, turma, nota):
        return self.repo.lancar_nota(aluno, turma, nota)

    def lancar_frequencia(self, aluno, turma, frequencia):
        return self.repo.lancar_frequencia(aluno, turma, frequencia)

    def concluir_matricula(self, aluno_id, turma_id):
        return self.repo.concluir_matricula(aluno_id, turma_id)

    def alunos_por_turma(self, id_turma):
        turma = self.repo.turmas.get(id_turma)
        if turma is None:
            return None

        alunos = []
        for m in turma.matriculas:
            aluno = self.repo.alunos.get(str(m.aluno))
            if aluno:
                alunos.append({
                    "matricula": aluno.matricula,
                    "nome": aluno.nome
                })

        return {
            "turma": id_turma,
            "curso": turma.codigo_curso,
            "ocupadas": len(alunos),
            "vagas": turma.vagas,
            "alunos": alunos
}
    #verificacoes

    def _verificar_prerequisitos(self, aluno, curso):
        codigos_aprovados = [
            item["codigo"]
            for item in aluno.historico
            if item.get("nota", 0) >= 6 and item.get("frequencia", 0) >= 75
        ]
        return all(req in codigos_aprovados for req in curso.prerequisitos)

    def _horarios_colidem(self, horario1, horario2):
        #formato {"seg": "10:00-12:00", "qua": "10:00-12:00"}
        for dia, intervalo1 in horario1.items():
            if dia in horario2:
                ini1, fim1 = intervalo1.split("-")
                ini2, fim2 = horario2[dia].split("-")
                if not (fim1 <= ini2 or fim2 <= ini1):
                    return True
        return False

    def _verificar_choque_horario(self, aluno, nova_turma):
        for m in self.repo.matriculas.values():
            if m.aluno == aluno.matricula:
                turma_atual = self.repo.turmas.get(m.turma)
                if turma_atual and turma_atual.periodo == nova_turma.periodo:
                    if self._horarios_colidem(turma_atual.horarios, nova_turma.horarios):
                        return True
        return False

    #matricula

    def matricular(self, matricula_aluno, id_turma):
        aluno = self.repo.alunos.get(matricula_aluno)
        turma = self.repo.turmas.get(id_turma)
        curso = self.repo.cursos.get(turma.codigo_curso)

        if aluno is None or turma is None:
            return False, "Aluno ou turma inexistente."

        if not self._verificar_prerequisitos(aluno, curso):
            return False, "Pré-requisitos não atendidos."

        if len(turma) >= turma.vagas:
            return False, "Turma lotada."

        if self._verificar_choque_horario(aluno, turma):
            return False, "Choque de horário detectado."

        #criar matrícula
        self.repo.add_matricula(matricula_aluno, id_turma)
        return True, "Matrícula realizada com sucesso."

    #relatorio
    
    def relatorio_alunos_por_turma(self):
        """Lista alunos por turma com vagas ocupadas vs totais."""
        resultado = []
        for turma_id, turma in self.repo.turmas.items():
            if isinstance(turma, dict):
                continue
            alunos = []
            for m in getattr(turma, "matriculas", []):
                aluno = self.repo.alunos.get(str(getattr(m, "aluno", m)))
                if aluno:
                    alunos.append({
                        "matricula": aluno.matricula,
                        "nome": aluno.nome
                    })
            resultado.append({
                "turma": turma_id,
                "curso": turma.codigo_curso,
                "ocupadas": len(alunos),
                "vagas": turma.vagas,
                "alunos": alunos
            })
        return resultado
    
    def relatorio_taxa_aprovacao(self):
        """Taxa de aprovação por curso e por turma."""
        import statistics
        nota_min = float(self.repo.cursos.get("nota_min", 6.0)) if isinstance(self.repo.cursos.get("nota_min"), (int, float)) else 6.0
        freq_min = 75.0
        
        # por turma
        por_turma = {}
        for turma_id, turma in self.repo.turmas.items():
            if isinstance(turma, dict):
                continue
            notas = []
            freqs = []
            for m in getattr(turma, "matriculas", []):
                if not isinstance(m, dict):
                    n = getattr(m, "nota", None)
                    f = getattr(m, "frequencia", None)
                    if n is not None and f is not None:
                        notas.append(n)
                        freqs.append(f)
            
            aprovados = sum(1 for n, f in zip(notas, freqs) if n >= nota_min and f >= freq_min)
            total = len(notas)
            taxa = (aprovados / total * 100) if total > 0 else 0
            
            por_turma[turma_id] = {
                "turma": turma_id,
                "curso": turma.codigo_curso,
                "aprovados": aprovados,
                "total": total,
                "taxa": round(taxa, 2)
            }
        
        # por curso
        por_curso = {}
        for turma_id, info in por_turma.items():
            curso = info["curso"]
            if curso not in por_curso:
                por_curso[curso] = {"aprovados": 0, "total": 0}
            por_curso[curso]["aprovados"] += info["aprovados"]
            por_curso[curso]["total"] += info["total"]
        
        for curso, info in por_curso.items():
            taxa = (info["aprovados"] / info["total"] * 100) if info["total"] > 0 else 0
            por_curso[curso]["taxa"] = round(taxa, 2)
        
        return {"por_turma": list(por_turma.values()), "por_curso": [{"curso": k, **v} for k, v in por_curso.items()]}
    
    def relatorio_distribuicao_notas(self):
        """Distribuição de notas por turma (média, mediana, desvio padrão)."""
        import statistics
        resultado = []
        
        for turma_id, turma in self.repo.turmas.items():
            if isinstance(turma, dict):
                continue
            notas = []
            for m in getattr(turma, "matriculas", []):
                if not isinstance(m, dict):
                    n = getattr(m, "nota", None)
                    if n is not None:
                        notas.append(n)
            
            if notas:
                media = statistics.mean(notas)
                mediana = statistics.median(notas)
                desvio = statistics.stdev(notas) if len(notas) > 1 else 0
                resultado.append({
                    "turma": turma_id,
                    "curso": turma.codigo_curso,
                    "media": round(media, 2),
                    "mediana": round(mediana, 2),
                    "desvio_padrao": round(desvio, 2),
                    "quantidade": len(notas)
                })
        
        return resultado
    
    def relatorio_alunos_risco(self):
        """Alunos com notq parcial < corte ou frequência < mínimo."""
        nota_min = 6.0
        freq_min = 75.0
        resultado = []
        
        for turma_id, turma in self.repo.turmas.items():
            if isinstance(turma, dict):
                continue
            for m in getattr(turma, "matriculas", []):
                if not isinstance(m, dict):
                    nota = getattr(m, "nota", None)
                    freq = getattr(m, "frequencia", None)
                    aluno_id = getattr(m, "aluno", m)
                    
                    # Aluno em risco se nota < min OU freq < min
                    if (nota is not None and nota < nota_min) or (freq is not None and freq < freq_min):
                        aluno = self.repo.alunos.get(str(aluno_id))
                        resultado.append({
                            "aluno": aluno.nome if aluno else str(aluno_id),
                            "matricula": aluno.matricula if aluno else str(aluno_id),
                            "turma": turma_id,
                            "curso": turma.codigo_curso,
                            "nota": nota,
                            "frequencia": freq,
                            "motivo": "Nota baixa" if nota and nota < nota_min else "Frequência baixa"
                        })
        
        return resultado
    
    def relatorio_top_alunos_cr(self, top_n=10):
        """Top N alunos por coeficiente"""
        alunos_com_cr = []
        
        for mat, aluno in self.repo.alunos.items():
            if isinstance(aluno, dict):
                continue
            historico = getattr(aluno, "historico", [])
            if historico:
                cr = aluno.cr  # prop da classe Aluno
                alunos_com_cr.append({
                    "matricula": aluno.matricula,
                    "nome": aluno.nome,
                    "cr": round(cr, 2),
                    "cursos_concluidos": len(historico)
                })
        
        # em ordem crescente
        alunos_com_cr.sort(key=lambda x: x["cr"], reverse=True)
        return alunos_com_cr[:top_n]