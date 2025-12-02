from flask import Flask, jsonify, request
from src.core.repository import Repository
from src.core.reports import Reports

app = Flask(__name__)

repo = Repository()
reports = Reports(repo)

@app.route("/")
def index():
    return jsonify({"status": "ok", "mensagem": "funcionando"})

@app.route("/alunos", methods=["GET"])
def listar_alunos():
    alunos = repo.list_alunos()
    return jsonify([aluno.to_dict() for aluno in alunos])

@app.route("/alunos", methods=["POST"])
def criar_aluno():
    dados = request.json
    aluno = repo.add_aluno(
        matricula=dados["matricula"],
        nome=dados["nome"],
        idade=dados.get("idade"),
        curso=dados.get("curso")
    )
    return jsonify(aluno.to_dict()), 201

@app.route("/turmas", methods=["GET"])
def listar_turmas():
    turmas = repo.list_turmas()
    return jsonify([turma.to_dict() for turma in turmas])

@app.route("/matriculas", methods=["POST"])
def criar_matricula():
    dados = request.json
    matricula = repo.add_matricula(
        aluno_matricula=dados["aluno"],
        turma_codigo=dados["turma"]
    )
    return jsonify(matricula.to_dict()), 201

@app.route("/relatorio/turma/<codigo>", methods=["GET"])
def relatorio_turma(codigo):
    resultado = reports.alunos_por_turma(codigo)
    if resultado is None:
        return jsonify({"erro": "Turma não encontrada"}), 404
    return jsonify(resultado)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
