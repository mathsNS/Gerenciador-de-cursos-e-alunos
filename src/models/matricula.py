class Matricula:
    def __init__(self, aluno, turma):
        self.aluno = aluno
        self.turma = turma
        self.nota = None
        self.frequencia = None
        self.ativa = True

    @property
    def situacao(self):
        if not self.ativa:
            return "TRANCADA"
        if self.nota is None or self.frequencia is None:
            return "CURSANDO"
        if self.nota < 6:
            return "REPROVADO_POR_NOTA"
        if self.frequencia < 75:
            return "REPROVADO_POR_FREQUENCIA"
        return "APROVADO"

    def __eq__(self, other):
        return isinstance(other, Matricula) and \
               other.aluno.matricula == self.aluno.matricula and \
               other.turma.id_turma == self.turma.id_turma
