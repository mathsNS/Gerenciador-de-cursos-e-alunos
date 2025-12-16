from fastapi import APIRouter
from pydantic import BaseModel
from src.core.container import sistema
from src.core.repository import Repository

router = APIRouter(prefix="/turmas", tags=["Turmas"])

@router.get("/")
def listar_turmas():
    resultado = []

    for t in sistema.repo.turmas.values():
        alunos = []
        if hasattr(t, "matriculas"):
            for m in t.matriculas:
                aluno = sistema.repo.alunos.get(str(m.aluno))
                if aluno:
                    alunos.append({
                        "matricula": aluno.matricula,
                        "nome": aluno.nome
                    })

        resultado.append({
            "id_turma": t.id_turma,
            "codigo_curso": t.codigo_curso,
            "periodo": t.periodo,
            "horarios": t.horarios,
            "vagas": t.vagas,
            "ocupadas": len(t.matriculas) if hasattr(t, "matriculas") else 0,
            "alunos": list(sistema.repo.alunos.values())
        })

    return resultado
