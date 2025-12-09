from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import sistema


router = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.get("/")
def listar_turmas():
    return list(sistema.repo.turmas.values())
