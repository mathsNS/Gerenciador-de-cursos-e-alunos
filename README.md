
# **Gerenciador de Cursos e Alunos**

## **Descrição do Projeto**

Sistema acadêmico em Python, com interface **CLI** (linha de comando), voltado para o gerenciamento de cursos, turmas, alunos e matrículas.
Inclui controle de pré-requisitos, vagas, choque de horários, notas, frequência, cálculo de CR, além de relatórios acadêmicos.
O foco é aplicar de forma sólida os princípios de **Programação Orientada a Objetos**: herança, encapsulamento, métodos especiais e validações.

---

## **Objetivo**

Implementar um sistema completo seguindo todos os requisitos definidos no documento oficial do projeto, aplicando:

* Estruturação OO com classes bem definidas
* Relacionamentos entre entidades
* Configurações e regras acadêmicas
* Persistência em JSON ou SQLite
* Testes automatizados com pytest
* Interface mínima via CLI

O objetivo central é consolidar o domínio de **POO em Python**, incluindo uso correto de propriedades, validações, herança e métodos especiais.

---

## **Arquitetura**

A arquitetura segue uma divisão simples e objetiva:

```
Entrada do usuário (CLI)
      ↓
Camada de Serviços (regras de negócio)
      ↓
Modelos de Dados (entidades)
      ↓
Persistência (JSON ou SQLite)
```

---

## **UML — Visão Geral Textual das Classes**

### **1. Pessoa (base)**

* Atributos: nome, email
* Herdada por: **Aluno**

### **2. Aluno (Pessoa)**

* Atributos: matrícula, histórico (notas + frequência), CR
* Métodos: cálculo de CR
* Método especial: `__lt__` para ordenação por CR
* Relacionamento: possui várias **Matrículas**

### **3. Curso**

* Atributos: código, nome, carga horária, pré-requisitos
* Método especial: `__str__` e `__repr__`
* Validações: evitar ciclos de pré-requisitos

### **4. Oferta (base)**

* Atributos: semestre, horários
* Herdada por: **Turma**

### **5. Turma (Oferta)**

* Atributos: id, vagas, local, lista de alunos
* Métodos: abrir/fechar, verificar choque de horários
* Método especial: `__len__` → retorna ocupação atual
* Relacionamento: está vinculada a um **Curso**

### **6. Matrícula**

* Atributos: notas, frequência, situação
* Métodos: lançar nota, lançar frequência, calcular situação
* Método especial: `__eq__` (aluno + turma)
* Relacionamento: conecta **Aluno** ↔ **Turma**

---

## **Organização das Pastas**

```
projeto_academico/
├── README.md
├── settings.json
│
├── models/
│   ├── __init__.py
│   ├── pessoa.py
│   ├── aluno.py
│   ├── curso.py
│   ├── oferta.py
│   ├── turma.py
│   └── matricula.py
│
├── services/
│   ├── __init__.py
│   ├── cadastro_service.py
│   └── matricula_service.py
│
├── data/
│   ├── __init__.py
│   ├── dados.py
│   └── seed.py
│
├── cli/
│   ├── __init__.py
│   └── main.py
│
└── tests/
    ├── __init__.py
    └── test_matricula.py
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

* **JSON** (persistência simples)
  ou
* **SQLite** (via `sqlite3`)

O módulo `dados.py` abstrai leitura/escrita.

---

## **Como Rodar**

Pré-requisitos:

```
Python 3.11+
```

Rodar via CLI:

```
python -m cli.main
```

Rodar testes:

```
pytest
```

---
