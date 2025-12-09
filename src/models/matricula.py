from enum import Enum

class EstadoMatricula(Enum):
    CURSANDO = "CURSANDO"
    APROVADO = "APROVADO"
    REPROVADO_POR_NOTA = "REPROVADO_POR_NOTA"
    REPROVADO_POR_FREQUENCIA = "REPROVADO_POR_FREQUENCIA"
    TRANCADO = "TRANCADO"


class Matricula:
    def __init__(self, aluno, turma):
        self.aluno = aluno
        self.turma = turma
        self.nota = None
        self.frequencia = None
        self.estado = EstadoMatricula.CURSANDO   # estado inicial
        self.ativa = True

    def calcular_situacao(self, nota_min, freq_min):
        # se ja trancado, mantem
        if self.estado == EstadoMatricula.TRANCADO:
            return EstadoMatricula.TRANCADO

        # se faltam dados, ainda esta cursando
        if self.nota is None or self.frequencia is None:
            return EstadoMatricula.CURSANDO

        # regras p/ aprovar
        if self.frequencia < freq_min:
            return EstadoMatricula.REPROVADO_POR_FREQUENCIA
        if self.nota < nota_min:
            return EstadoMatricula.REPROVADO_POR_NOTA

        return EstadoMatricula.APROVADO

    @property
    def situacao(self):
        return self.estado.value

    def __eq__(self, other):
        return (
            isinstance(other, Matricula)
            and other.aluno == self.aluno
            and other.turma == self.turma
        )
