# testes para models, repository, persistencia e relatorios

import pytest
import tempfile
from src.models.aluno import Aluno
from src.models.curso import Curso
from src.models.turma import Turma
from src.models.matricula import Matricula, EstadoMatricula
from src.core.repository import Repository
from src.core.sistema import SistemaAcademico


@pytest.fixture
def temp_data_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def repo_test(temp_data_dir):
    return Repository(data_dir=temp_data_dir, mem=False)


@pytest.fixture
def sistema_test(temp_data_dir):
    repo = Repository(data_dir=temp_data_dir, mem=False)
    sistema = SistemaAcademico()
    sistema.repo = repo
    return sistema


def test_aluno_criar():
    aluno = Aluno(matricula="001", nome="Joao Silva", email="joao@email.com")
    assert aluno.matricula == "001"
    assert aluno.nome == "Joao Silva"
    assert aluno.historico == []


def test_aluno_adicionar_historico():
    aluno = Aluno(matricula="002", nome="Maria", email="maria@email.com")
    aluno.adicionar_historico(curso="MAT101", nota=8.5, frequencia=95.0)
    assert len(aluno.historico) == 1
    assert aluno.historico[0]["curso"] == "MAT101"
    assert aluno.historico[0]["nota"] == 8.5


def test_aluno_cr_calculo():
    aluno = Aluno(matricula="003", nome="Pedro", email="pedro@email.com")
    aluno.adicionar_historico(curso="MAT101", nota=8.0, frequencia=90.0)
    aluno.adicionar_historico(curso="FIS101", nota=7.0, frequencia=85.0)
    cr_esperado = (8.0 + 7.0) / 2
    assert aluno.cr == cr_esperado


def test_turma_criar():
    turma = Turma(
        id_turma="T1",
        codigo_curso="MAT101",
        periodo="2025.1",
        horarios={"seg": "10:00-12:00", "qua": "10:00-12:00"},
        vagas=30
    )
    assert turma.id_turma == "T1"
    assert turma.vagas == 30


def test_repository_lancar_nota(repo_test):
    aluno = repo_test.add_aluno("102", "Lucas", "lucas@email.com")
    repo_test.add_curso("FIS101", "Fisica I", 60, [])
    turma = repo_test.add_turma("T2", "FIS101", "2025.1", {}, 25)
    repo_test.add_matricula("102", "T2")
    
    ok, msg = repo_test.lancar_nota(aluno, turma, 8.5)
    assert ok is True


def test_repository_concluir_matricula(repo_test):
    aluno = repo_test.add_aluno("104", "Gabriel", "gabriel@email.com")
    repo_test.add_curso("BIO101", "Biologia I", 60, [])
    turma = repo_test.add_turma("T4", "BIO101", "2025.1", {}, 25)
    repo_test.add_matricula("104", "T4")
    
    repo_test.lancar_nota(aluno, turma, 7.5)
    repo_test.lancar_frequencia(aluno, turma, 85.0)
    ok, msg = repo_test.concluir_matricula("104", "T4")
    
    assert ok is True
    assert len(aluno.historico) == 1
    assert aluno.historico[0]["curso"] == "BIO101"


def test_repository_persistencia_historico(temp_data_dir):
    repo1 = Repository(data_dir=temp_data_dir, mem=False)
    aluno = repo1.add_aluno("202", "Renata", "renata@email.com")
    repo1.add_curso("MAT102", "Matematica II", 60, [])
    turma = repo1.add_turma("T5", "MAT102", "2025.1", {}, 25)
    repo1.add_matricula("202", "T5")
    repo1.lancar_nota(aluno, turma, 9.0)
    repo1.lancar_frequencia(aluno, turma, 95.0)
    repo1.concluir_matricula("202", "T5")
    repo1.save_all()
    
    repo2 = Repository(data_dir=temp_data_dir, mem=False)
    aluno_carregado = repo2.alunos["202"]
    
    assert isinstance(aluno_carregado.historico, list)
    assert len(aluno_carregado.historico) == 1
    assert aluno_carregado.historico[0]["curso"] == "MAT102"


def test_sistema_relatorio_alunos_por_turma(sistema_test):
    aluno = sistema_test.repo.add_aluno("301", "Thiago", "thiago@email.com")
    sistema_test.repo.add_curso("ENG101", "Engenharia I", 60, [])
    turma = sistema_test.repo.add_turma("T6", "ENG101", "2025.1", {}, 30)
    sistema_test.repo.add_matricula("301", "T6")
    
    relatorio = sistema_test.relatorio_alunos_por_turma()
    assert len(relatorio) > 0
    assert relatorio[0]["turma"] == "T6"
