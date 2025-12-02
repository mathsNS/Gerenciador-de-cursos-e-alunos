import os
import json

class Repository:

    def add_curso(self, codigo, nome, carga):
        from src.models.curso import Curso
        curso = Curso(codigo, nome, carga)
        self.cursos[codigo] = curso
        return curso

    def add_aluno(self, matricula, nome):
        from src.models.aluno import Aluno
        aluno = Aluno(matricula, nome)
        self.alunos[matricula] = aluno
        return aluno

    def add_turma(self, codigo, cod_curso, horario, vagas):
        from src.models.turma import Turma
        curso = self.cursos[cod_curso]
        turma = Turma(codigo, curso, horario, vagas)
        self.turmas[codigo] = turma
        return turma

    def __init__(self, mem=False):
        self.mem = mem

        self.cursos = {}
        self.turmas = {}
        self.alunos = {}
        self.matriculas = []

        if not self.mem:
            self._carregar()

    #persistencia

    def _read(self, filename):
        if self.mem:
            return {}  # evitar leitura quando mem=True

        if not os.path.exists(filename):
            return {}

        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _carregar(self):
        # cursos.json tem que ser dict
        for c in self._read("cursos.json").values():
            self.cursos[c["codigo"]] = c

        # turmas.json também
        for t in self._read("turmas.json").values():
            self.turmas[t["codigo"]] = t

        # alunos.json também
        for a in self._read("alunos.json").values():
            self.alunos[a["ra"]] = a

        # lista de matriculas
        self.matriculas = self._read("matriculas.json") or []

    def salvar(self):
        if self.mem:
            return  # no modo memória não salva

        with open("cursos.json", "w", encoding="utf-8") as f:
            json.dump(self.cursos, f, indent=4, ensure_ascii=False)

        with open("turmas.json", "w", encoding="utf-8") as f:
            json.dump(self.turmas, f, indent=4, ensure_ascii=False)

        with open("alunos.json", "w", encoding="utf-8") as f:
            json.dump(self.alunos, f, indent=4, ensure_ascii=False)

        with open("matriculas.json", "w", encoding="utf-8") as f:
            json.dump(self.matriculas, f, indent=4, ensure_ascii=False)
