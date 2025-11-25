class Curso:
    def __init__(self, codigo, nome, carga_horaria, prerequisitos=None, ementa=None):
        self.codigo = codigo
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.prerequisitos = prerequisitos or []
        self.ementa = ementa

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    def __repr__(self):
        return f"Curso(codigo='{self.codigo}', nome='{self.nome}')"
