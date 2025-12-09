from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import sistema

router = APIRouter(prefix="/alunos", tags=["Alunos"])

class CriarAlunoDTO(BaseModel):
    matricula: str
    nome: str
    idade: int

@router.get("/")
def listar_alunos():
    return list(sistema.repo.alunos.values())

@router.post("/")
def criar_aluno(dto: CriarAlunoDTO):
    if dto.matricula in sistema.repo.alunos:
        return {"erro": "Aluno já existe"}
    sistema.repo.alunos[dto.matricula] = dto.dict()
    sistema.repo._save_all()
    return {"status": "ok", "dados": dto}
