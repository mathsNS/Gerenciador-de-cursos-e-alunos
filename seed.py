from src.core.repository import Repository
from src.models.curso import Curso
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.core.db import repo


repo = Repository(mem=False)

repo.cursos = {
    "MAT101": Curso("MAT101", "Cálculo I", 60, []).__dict__,
    "FIS101": Curso("FIS101", "Física I", 60, ["MAT101"]).__dict__,
}

repo.alunos = {
    "1": Aluno("1", "João", "j@j.com").__dict__,
    "2": Aluno("2", "Maria", "m@m.com").__dict__,
}

repo.turmas = {
    "T1": Turma(
        id_turma="T1",
        codigo_curso="MAT101",
        periodo="2025.2",
        horarios={"seg": "08:00-10:00"},
        vagas=40,
        local="Bloco A"
    ).__dict__,

    "T2": Turma(
        id_turma="T2",
        codigo_curso="FIS101",
        periodo="2025.2",
        horarios={"seg": "08:00-10:00"},
        vagas=40,
        local="Bloco B"
    ).__dict__,
}

repo._write("cursos.json", repo.cursos)
repo._write("alunos.json", repo.alunos)
repo._write("turmas.json", repo.turmas)
repo._write("matriculas.json", {})
print("Seed carregado com sucesso.")
