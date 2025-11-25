class Matricula:
    def __init__(self, aluno, turma):
        self.aluno = aluno
        self.turma = turma
        self.nota = None
        self.frequencia = None
        self.estado = "CURSANDO"

    def __eq__(self, other):
        return (
            self.aluno.matricula == other.aluno.matricula
            and self.turma.id_turma == other.turma.id_turma
        )
