from fastapi import FastAPI
from src.core.container import sistema
from src.api import alunos, turmas, matriculas, relatorios, health

app = FastAPI()

app.include_router(alunos.router)
app.include_router(turmas.router)
app.include_router(matriculas.router)
app.include_router(relatorios.router)
app.include_router(health.router)

@app.get("/")
def root():
    return {"status": "ok", "mensagem": "API Funcionando"}
