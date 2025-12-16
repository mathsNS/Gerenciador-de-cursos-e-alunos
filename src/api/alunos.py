from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import sistema
from src.core.repository import Repository
from src.core.models import Aluno

router = APIRouter(prefix="/alunos", tags=["Alunos"])

class CriarAlunoDTO(BaseModel):
    matricula: str
    nome: str
    email: str
    historico: str
    cursos_concluidos: int


@router.get("/")
def listar_alunos():
    return list(sistema.repo.alunos.values())

@router.post("/")
def criar_aluno(dto: CriarAlunoDTO):
    if dto.matricula in sistema.repo.alunos:
        return {"erro": "Aluno já existe"}

    aluno = Aluno(
        matricula=dto.matricula,
        nome=dto.nome,
        email=dto.email,
        historico=dto.historico,
        cursos_concluidos=dto.cursos_concluidos
    )

    sistema.repo.alunos[aluno.matricula] = aluno
    sistema.repo.save_all()

    return aluno
