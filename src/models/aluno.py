class Pessoa:
    def __init__(self, nome, email):
        self._nome = nome
        self._email = email

    @property
    def nome(self):
        return self._nome

    @property
    def email(self):
        return self._email


class Aluno:
    def __init__(self, matricula, nome, email=None):
        self.matricula = matricula
        self.nome = nome
        self.email = email
        self.cursos_concluidos = [] # lista de dicts: {"curso": "ABC123", "nota": x, "frequencia": y}

    def adicionar_historico(self, curso, nota, frequencia):
        self.historico.append({
            "curso": curso,
            "nota": nota,
            "frequencia": frequencia
        })

    @property
    def cr(self):
        if not self.historico:
            return 0
        soma = sum(item["nota"] for item in self.historico)
        return soma / len(self.historico)

    def __lt__(self, other):
        if not isinstance(other, Aluno):
            return False
        return self.cr < other.cr
    
