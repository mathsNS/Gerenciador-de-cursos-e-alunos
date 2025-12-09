import pytest 
from src.models.aluno import Aluno
from src.core.repository import Repository

def test_criacao_aluno():
    a = Aluno(matricula="2025001", nome="João", email="j@ex.com")
    assert a.matricula == "2025001"
    assert a.nome == "João"
    assert a.email == "j@ex.com"
    assert a.historico == []

def test_cr_medio_simples():
    a = Aluno("1", "Teste", "t@t.com")
    a.historico = [
        {"codigo": "MAT", "nota": 8, "frequencia": 90},
        {"codigo": "POR", "nota": 6, "frequencia": 80},
        {"codigo": "HIS", "nota": 10, "frequencia": 100}
    ]
    cr = a.cr
    assert cr == pytest.approx((8+6+10)/3)
