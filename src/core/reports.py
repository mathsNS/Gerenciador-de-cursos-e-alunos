
class Reports:
    def __init__(self, repo):
        self.repo = repo

    def alunos_por_turma(self, codigo_turma):
        turma = self.repo.get_turma(codigo_turma)
        if turma is None:
            return None

        alunos = []
        for matricula in self.repo.list_matriculas():
            if matricula.codigo_turma == codigo_turma:
                aluno = self.repo.get_aluno(matricula.matricula)
                if aluno:
                    alunos.append({
                        "matricula": aluno.matricula,
                        "nome": aluno.nome
                    })

        return {
            "turma": codigo_turma,
            "curso": turma.curso,
            "capacidade": turma.capacidade,
            "alunos_matriculados": alunos,
            "quantidade": len(alunos)
        }
