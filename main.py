from src.core.repository import Repository
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from src.api import alunos, turmas, matriculas, relatorios, health
from src.api import ui
from src.core.sistema import SistemaAcademico


app = FastAPI(title="Sistema Acadêmico")
repo = Repository()

# objeto global para toda API
sistema = SistemaAcademico()

# inclui as rotas
app.include_router(health.router)
app.include_router(alunos.router)
app.include_router(turmas.router)
app.include_router(matriculas.router)
app.include_router(relatorios.router)
app.include_router(ui.router, prefix="/ui")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    # redireciona pra interface
    return RedirectResponse(url="/ui/")
