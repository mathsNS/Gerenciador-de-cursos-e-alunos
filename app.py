from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"status": "ok", "mensagem": "funcionando"})

# Rota básica para listar alunos (temporaria enquanto nao integra)
@app.route("/alunos", methods=["GET"])
def listar_alunos():
    return jsonify({"alunos": []})

# Rota para criar aluno (estrutura simples pra teste)
@app.route("/alunos", methods=["POST"])
def criar_aluno():
    dados = request.json
    return jsonify({
        "status": "recebido",
        "dados": dados
    }), 201

# Rota básica de saude(status) do sistema
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
