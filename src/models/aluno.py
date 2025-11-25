class Aluno:
    def __init__(self, matricula, nome, email):
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.historico = []

    @property
    def cr(self):
        if not self.historico:
            return 0
        notas = [item["nota"] for item in self.historico]
        return sum(notas) / len(notas)
