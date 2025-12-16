from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates
from src.core.container import sistema

router = APIRouter(tags=["UI"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/alunos", response_class=HTMLResponse)
def listar_alunos(request: Request):
    raw = list(sistema.repo.alunos.values())
    alunos = []
    for a in raw:
        if isinstance(a, dict):
            alunos.append(a)
        else:
            alunos.append({
                "matricula": getattr(a, "matricula", None),
                "nome": getattr(a, "nome", None),
                "email": getattr(a, "email", None),
                "historico": getattr(a, "historico", [])
            })

    return templates.TemplateResponse("alunos.html", {"request": request, "alunos": alunos})


@router.get("/alunos/{matricula}", response_class=HTMLResponse)
def perfil_aluno(request: Request, matricula: str):
    aluno = sistema.repo.alunos.get(str(matricula))
    if aluno is None:
        return templates.TemplateResponse("aluno_nao_encontrado.html", {"request": request, "matricula": matricula})

    # monta histórico e matrículas
    matriculas_raw = [m for m in sistema.repo.matriculas.values() if getattr(m, "aluno", None) and getattr(getattr(m, 'aluno'), "matricula", m.aluno) == str(matricula)]

    return templates.TemplateResponse("aluno_profile.html", {"request": request, "aluno": aluno, "matriculas": matriculas_raw})


@router.get("/turmas", response_class=HTMLResponse)
def listar_turmas(request: Request):
    turmas_raw = list(sistema.repo.turmas.values())
    turmas = []
    for t in turmas_raw:
        if isinstance(t, dict):
            turmas.append(t)
        else:
            turmas.append({
                "id_turma": getattr(t, "id_turma", None),
                "codigo_curso": getattr(t, "codigo_curso", None),
                "periodo": getattr(t, "periodo", None),
                "vagas": getattr(t, "vagas", None)
            })
    return templates.TemplateResponse("turmas.html", {"request": request, "turmas": turmas})


@router.get("/cursos", response_class=HTMLResponse)
def listar_cursos(request: Request):
    cursos_raw = list(sistema.repo.cursos.values())
    cursos = []
    for c in cursos_raw:
        if isinstance(c, dict):
            cursos.append(c)
        else:
            cursos.append({
                "codigo": getattr(c, "codigo", None),
                "nome": getattr(c, "nome", None),
                "carga_horaria": getattr(c, "carga_horaria", None)
            })
    return templates.TemplateResponse("cursos.html", {"request": request, "cursos": cursos})


@router.get("/relatorios", response_class=HTMLResponse)
def relatorios(request: Request):
    # gerar relatorio alunos por turma
    turmas = list(sistema.repo.turmas.keys())
    rels = []
    for t in turmas:
        dados = sistema.alunos_por_turma(t)
        if dados:
            rels.append(dados)

    return templates.TemplateResponse("relatorios.html", {"request": request, "relatorios": rels})


@router.post("/lancar_nota")
def ui_lancar_nota(matricula: str = Form(...), turma: str = Form(...), nota: float = Form(...)):
    aluno_obj = sistema.repo.alunos.get(matricula)
    turma_obj = sistema.repo.turmas.get(turma)
    if aluno_obj is None or turma_obj is None:
        return RedirectResponse(url=f"/ui/alunos/{matricula}", status_code=303)
    ok, msg = sistema.lancar_nota(aluno_obj, turma_obj, nota)
    return RedirectResponse(url=f"/ui/alunos/{matricula}", status_code=303)


@router.post("/lancar_frequencia")
def ui_lancar_frequencia(matricula: str = Form(...), turma: str = Form(...), frequencia: float = Form(...)):
    aluno_obj = sistema.repo.alunos.get(matricula)
    turma_obj = sistema.repo.turmas.get(turma)
    if aluno_obj is None or turma_obj is None:
        return RedirectResponse(url=f"/ui/alunos/{matricula}", status_code=303)
    ok, msg = sistema.lancar_frequencia(aluno_obj, turma_obj, frequencia)
    return RedirectResponse(url=f"/ui/alunos/{matricula}", status_code=303)


@router.post("/concluir_matricula")
def ui_concluir_matricula(matricula: str = Form(...), turma: str = Form(...)):
    ok, msg = sistema.concluir_matricula(matricula, turma)
    return RedirectResponse(url=f"/ui/alunos/{matricula}", status_code=303)
