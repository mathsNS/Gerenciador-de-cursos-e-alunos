import pytest
from src.models.curso import Curso
from src.models.aluno import Aluno
from src.models.turma import Turma
from src.models.matricula import Matricula
from src.core.repository import Repository

@pytest.fixture
def repo():
    return Repository(mem=True)  # versão em memória para testes


@pytest.fixture
def aluno_base():
    return Aluno(matricula="A1", nome="Matheus")


@pytest.fixture
def curso_base():
    return {
        "codigo": "POO101",
        "nome": "POO",
        "carga_horaria": 60,
        "prerequisitos": []
    }


#teste 1
def test_matricula_falha_por_prerequisito(repo, aluno_base):
    repo.add_curso("ALG100", "Algoritmos", 60)
    repo.add_curso("POO200", "POO", 60, prerequisitos=["ALG100"])

    repo.add_aluno("A1", "Matheus")
    repo.add_turma("T1", "POO200", "2025.1", {"seg": "10-12"}, vagas=30)

    with pytest.raises(ValueError):
        repo.add_matricula("A1", "T1")  # aluno não cursou ALG100


#teste 2
def test_matricula_falha_por_choque_horario(repo):
    repo.add_curso("C1", "Curso 1", 60)
    repo.add_curso("C2", "Curso 2", 60)

    repo.add_aluno("A1", "Matheus")

    repo.add_turma("T1", "C1", "2025.1", {"seg": "10-12"}, 40)
    repo.add_turma("T2", "C2", "2025.1", {"seg": "10-12"}, 40)

    repo.add_matricula("A1", "T1")

    with pytest.raises(ValueError):
        repo.add_matricula("A1", "T2")  # choque de horário


#teste 3
def test_matricula_falha_por_turma_lotada(repo):
    repo.add_curso("C1", "Curso", 60)
    repo.add_turma("T1", "C1", "2025.1", {"ter": "14-16"}, vagas=1)

    repo.add_aluno("A1", "Primeiro")
    repo.add_aluno("A2", "Segundo")

    repo.add_matricula("A1", "T1")

    with pytest.raises(ValueError):
        repo.add_matricula("A2", "T1")  # vagas esgotadas


#teste 4
def test_persistencia_json_simples(tmp_path):
    from src.core.dados import salvar_json, carregar_json

    arquivo = tmp_path / "dados.json"

    salvar_json(arquivo, {"x": 123})
    data = carregar_json(arquivo)

    assert data == {"x": 123}


#teste 5
def test_relatorio_alunos_por_turma(repo):
    repo.add_curso("C1", "Curso", 60)
    repo.add_turma("T1", "C1", "2025.1", {"qua": "08-10"}, vagas=10)

    repo.add_aluno("A1", "Aluno 1")
    repo.add_aluno("A2", "Aluno 2")

    repo.add_matricula("A1", "T1")
    repo.add_matricula("A2", "T1")

    rel = repo.alunos_por_turma("T1")

    assert rel["turma"] == "T1"
    assert rel["total"] == 2
    assert rel["alunos"] == ["A1", "A2"]
