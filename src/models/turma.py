class Turma:
    def __init__(self, id_turma, codigo_curso, periodo, horarios, vagas, local=None):
        self.id_turma = id_turma
        self.codigo_curso = codigo_curso
        self.periodo = periodo
        self.horarios = horarios  # {"ter":"10:00-12:00"}
        self.vagas = vagas
        self.local = local
        self.matriculas = []
        self.aberta = True

    def __len__(self):
        return len([m for m in self.matriculas if m.ativa])

    def tem_vaga(self):
        return len(self) < self.vagas

    def fechar(self):
        self.aberta = False
