from flask import Flask, jsonify, request
from src.core.repository import Repository
from src.core.reports import Reports
from src.core.sistema import Sistema

app = Flask(__name__)
sistema = Sistema()
repo = Repository()
reports = Reports(repo)

# lançar nota
@app.route("/matricula/lancar-nota", methods=["POST"])
def api_lancar_nota():
    data = request.json or {}
    aluno = data.get("aluno")
    turma = data.get("turma")
    nota = data.get("nota")
    ok, msg = sistema.lancar_nota(aluno, turma, nota)
    status = 200 if ok else 400
    return jsonify({"ok": ok, "mensagem": msg}), status

# lançar frequencia
@app.route("/matricula/lancar-frequencia", methods=["POST"])
def api_lancar_frequencia():
    data = request.json or {}
    aluno = data.get("aluno")
    turma = data.get("turma")
    frequencia = data.get("frequencia")
    ok, msg = sistema.lancar_frequencia(aluno, turma, frequencia)
    status = 200 if ok else 400
    return jsonify({"ok": ok, "mensagem": msg}), status

# trancar matricula
@app.route("/matricula/trancar", methods=["POST"])
def api_trancar():
    data = request.json or {}
    aluno = data.get("aluno")
    turma = data.get("turma")
    ok, msg = sistema.trancar_matricula(aluno, turma)
    status = 200 if ok else 400
    return jsonify({"ok": ok, "mensagem": msg}), status

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
