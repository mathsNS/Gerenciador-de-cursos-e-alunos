
# **Gerenciador de Cursos e Alunos**
![Status](https://img.shields.io/badge/Projeto-Semana%205-purple)
![Python](https://img.shields.io/badge/Python-3.11+-blue)

## **Descrição do Projeto**

Sistema acadêmico em Python, voltado para o gerenciamento de cursos, turmas, alunos e matrículas.
Inclui controle de pré-requisitos, vagas, choque de horários, notas, frequência, cálculo de CR, além de relatórios acadêmicos.
O foco é aplicar de forma sólida os princípios de Programação Orientada a Objetos: herança, encapsulamento, métodos especiais e validações.

---

## **Objetivo**

Implementar um sistema completo seguindo todos os requisitos definidos no documento oficial do projeto, aplicando:

* Estruturação OO com classes bem definidas
* Relacionamentos entre entidades(1:1, 1:N, N:M)
* Configurações e regras acadêmicas
* Persistência em JSON ou SQLite
* Testes automatizados com pytest
* Interface mínima via CLI
---

O objetivo central é consolidar o domínio de POO em Python, incluindo uso correto de propriedades, validações, herança e métodos especiais.
Uma etapa do projeto é realizada por semana, com os commits finais de cada semana de desenvolvimento explicitados.

## **FastAPI**

FastAPI é um framework moderno para criação de APIs em Python, focado em alta performance e validação automática de dados. Ele utiliza tipagem padrão do Python para gerar documentação interativa em tempo real (Swagger e Redoc) e facilita a criação de endpoints organizados para operações como matrícula, lançamento de notas e frequência. No projeto, o FastAPI funciona como a interface de acesso ao sistema, expondo rotas que acionam as regras de negócio implementadas no núcleo da aplicação. Essa camada permite integração com clientes externos, testes via HTTP e uso prático das funcionalidades do gerenciador acadêmico.

## **Arquitetura**

A arquitetura segue uma divisão simples e objetiva:

```
Entrada do usuário
      
Camada de Serviços (regras de negócio)
      
Modelos de Dados (entidades)
      
Persistência (JSON ou SQLite)
```

---

## **UML — Visão Geral Textual das Classes**

### **1. Pessoa (base)**

* Atributos: nome, email
* Herdada por: **Aluno**
* Relacionamentos: 1:N com Aluno (uma pessoa → um aluno)

### **2. Aluno (Pessoa)**

* Atributos: matrícula, histórico (notas + frequência), CR
* Métodos: cálculo de CR
* Método especial: `__lt__` para ordenação por CR
* Relacionamentos: 1:N com Matricula (um aluno → várias matrículas)

### **3. Curso**

* Atributos: código, nome, carga horária, pré-requisitos
* Método especial: `__str__` e `__repr__`
* Validações: evitar ciclos de pré-requisitos
* Relacionamentos: 1:N com Turma (um curso → várias turmas)

### **4. Oferta (base)**

* Atributos: semestre, horários
* Herdada por: **Turma**

### **5. Turma (Oferta)**

* Atributos: id, vagas, local, lista de alunos
* Métodos: abrir/fechar, verificar choque de horários
* Método especial: `__len__` → retorna ocupação atual
* Relacionamentos: N:1 com Curso; 1:N com Matricula (uma turma → várias matrículas)

### **6. Matrícula**

* Atributos: notas, frequência, situação
* Métodos: lançar nota, lançar frequência, calcular situação
* Método especial: `__eq__` (aluno + turma)
* Relacionamentos: conecta Aluno ↔ Turma (N:M via matrícula)

---

## **Organização das Pastas**

```
gerenciador-poo/
├── README.md
├── LICENSE
├── requirements.txt
├── settings.json
├── main.py (entry point FastAPI)
├── seed.py (popular dados iniciais)
│
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pessoa.py
│   │   ├── aluno.py
│   │   ├── curso.py
│   │   ├── horario.py
│   │   ├── oferta.py
│   │   ├── turma.py
│   │   └── matricula.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── container.py (singleton SistemaAcademico)
│   │   ├── repository.py (CRUD + persistência JSON)
│   │   ├── sistema.py (lógica de negócio + relatórios)
│   │   ├── dados.py
│   │   ├── db.py
│   │   ├── models.py
│   │   ├── reports.py
│   │   ├── scheduler.py
│   │   └── validators.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── ui.py (rotas HTML + formulários)
│       ├── alunos.py (endpoints JSON)
│       ├── turmas.py
│       ├── matriculas.py
│       ├── relatorios.py
│       └── health.py
│
├── data/
│   ├── alunos.json
│   ├── cursos.json
│   ├── turmas.json
│   └── matriculas.json
│
├── templates/
│   ├── base.html (layout base com navbar)
│   ├── index.html
│   ├── alunos.html (lista + form criar aluno)
│   ├── aluno_profile.html (perfil, histórico, matrículas, formulários)
│   ├── turmas.html (lista turmas)
│   ├── cursos.html (lista + form criar curso)
│   └── relatorios.html (5 relatórios consolidados)
│
├── static/
│   └── style.css
│
└── tests/
    ├── __init__.py
    ├── test_aluno.py
    ├── test_curso.py
    ├── test_turma.py
    ├── test_matricula.py
    ├── test_horario.py
    ├── test_cr.py
    ├── test_sistema_completo.py
    └── __pycache__/
```

---

## **Funcionalidades Principais**

* Cadastro de cursos, alunos e turmas
* Matrícula com validação de:

  * Pré-requisitos
  * Vagas disponíveis
  * Choque de horários
* Lançamento de notas e frequência
* Cálculo de situação acadêmica
* Cálculo de CR
* Relatórios:

  * Taxa de aprovação
  * Distribuição de notas
  * Top N alunos por CR

---

## **Persistência**

O projeto pode usar:

* JSON (persistência simples)

O módulo `dados.py` abstrai leitura/escrita.

---

## **Como Rodar**

Pré-requisitos:

```
Python 3.11+
Uvicorn
```
Instalar dependências:

```
pip install -r requirements.txt
```

Rodar testes:

```
pytest
```

Rodar sistema: 

```
uvicorn main:app --reload
```

O comando abaixo inicia a aplicação e disponibiliza a documentação automática em /docs (Swagger UI) e /redoc:
A interface para navegação pode ser acessada em /ui

---








