class Turma:
    def __init__(self, id_turma, codigo_curso, periodo, horarios, vagas):
        self.id_turma = id_turma
        self.codigo_curso = codigo_curso
        self.periodo = periodo
        self.horarios = horarios
        self.vagas = vagas
        self.matriculas = []

    def __len__(self):
        return len(self.matriculas)

    @property
    def vagas_disponiveis(self):
        return self.vagas - len(self.matriculas)
