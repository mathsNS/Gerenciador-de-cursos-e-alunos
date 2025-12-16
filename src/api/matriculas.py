from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import sistema
from src.core.repository import Repository
from fastapi import HTTPException

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

class MatricularDTO(BaseModel):
    matricula_aluno: str
    id_turma: str


class NotaDTO(BaseModel):
    nota: float

class FrequenciaDTO(BaseModel):
    frequencia: float


@router.post("/matriculas/")
def criar_matricula(dados: MatricularDTO):
    try:
        matricula = sistema.repo.add_matricula(
            aluno_id=dados.matricula_aluno,
            turma_id=dados.id_turma
        )
        return {"status": "ok", "matricula": f"{dados.matricula_aluno}_{dados.id_turma}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{aluno}/{turma}/nota")
def lancar_nota(aluno: str, turma: str, body: NotaDTO):
    aluno_obj = sistema.repo.alunos.get(aluno)
    turma_obj = sistema.repo.turmas.get(turma)

    if aluno_obj is None or turma_obj is None:
        return {"sucesso": False, "mensagem": "Aluno ou turma não encontrados"}

    ok, msg = sistema.lancar_nota(aluno_obj, turma_obj, body.nota)
    return {"sucesso": ok, "mensagem": msg}


@router.post("/{aluno}/{turma}/frequencia")
def lancar_frequencia(aluno: str, turma: str, body: FrequenciaDTO):
    aluno_obj = sistema.repo.alunos.get(aluno)
    turma_obj = sistema.repo.turmas.get(turma)

    if aluno_obj is None or turma_obj is None:
        return {"sucesso": False, "mensagem": "Aluno ou turma não encontrados"}

    ok, msg = sistema.lancar_frequencia(aluno_obj, turma_obj, body.frequencia)
    return {"sucesso": ok, "mensagem": msg}
