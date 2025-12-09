import pytest
from src.models.curso import Curso
from src.core.repository import Repository

def test_criacao_curso_basico():
    c = Curso(codigo="MAT101", nome="Cálculo I", carga_horaria=60)
    assert c.codigo == "MAT101"
    assert c.nome == "Cálculo I"
    assert c.carga_horaria == 60
    assert c.prerequisitos == []

def test_curso_repr():
    c = Curso(codigo="POO200", nome="POO", carga_horaria=80)
    texto = repr(c)
    assert "POO200" in texto
    assert "POO" in texto
