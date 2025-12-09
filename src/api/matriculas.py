from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import sistema

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

class MatricularDTO(BaseModel):
    aluno: str
    turma: str

class NotaDTO(BaseModel):
    nota: float

class FrequenciaDTO(BaseModel):
    frequencia: float


@router.post("/")
def criar_matricula(dto: MatricularDTO):
    aluno = sistema.repo.alunos.get(dto.aluno)
    turma = sistema.repo.turmas.get(dto.turma)

    if aluno is None or turma is None:
        return {"sucesso": False, "mensagem": "Aluno ou turma não encontrados"}

    ok, msg = sistema.matricular(aluno, turma)
    return {"sucesso": ok, "mensagem": msg}


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
