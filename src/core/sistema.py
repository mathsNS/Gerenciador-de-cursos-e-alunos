from src.core.repository import Repository
from src.models.matricula import Matricula


class SistemaAcademico:
    def __init__(self):
        self.repo = Repository()

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
            if m.aluno == aluno.matricula and m.turma.periodo == nova_turma.periodo:
                if self._horarios_colidem(m.turma.horarios, nova_turma.horarios):
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
        nova = Matricula(aluno=aluno.matricula, turma=turma.id_turma)
        self.repo.adicionar_matricula(nova)

        return True, "Matrícula realizada com sucesso."

    #relatorio

    def alunos_por_turma(self, id_turma):
        turma = self.repo.turmas.get(id_turma)
        if turma is None:
            return None

        alunos = [
            self.repo.alunos[m.aluno].nome
            for m in self.repo.matriculas.values()
            if m.turma == id_turma
        ]

        return {
            "turma": id_turma,
            "curso": turma.codigo_curso,
            "ocupadas": len(alunos),
            "vagas": turma.vagas,
            "alunos": alunos
        }
