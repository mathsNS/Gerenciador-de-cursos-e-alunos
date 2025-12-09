from fastapi import APIRouter
from src.core.container import sistema

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])

@router.get("/turma/{id_turma}")
def relatorio_turma(id_turma: str):
    dados = sistema.alunos_por_turma(id_turma)
    if dados is None:
        return {"erro": "Turma não encontrada"}
    return dados
