from flask import Blueprint, request, jsonify, session
from models import Usuario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados não enviados"}), 400

    email = dados.get("email", "").strip().lower()
    senha = dados.get("senha", "").strip()

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    if not usuario.verificar_senha(senha):
        return jsonify({"erro": "Senha inválida"}), 401

    session["usuario_id"] = usuario.id
    session["usuario_nome"] = usuario.nome
    session["usuario_email"] = usuario.email
    session["usuario_tipo"] = usuario.tipo
    session["congregacao_id"] = usuario.congregacao_id

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "tipo": usuario.tipo,
            "congregacao_id": usuario.congregacao_id
        }
    }), 200

@auth_bp.route("/me", methods=["GET"])
def me():
    if "usuario_id" not in session:
        return jsonify({"erro": "Não autenticado"}), 401

    usuario = Usuario.query.get(session["usuario_id"])

    if not usuario:
        session.clear()
        return jsonify({"erro": "Usuário não encontrado"}), 404

    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "tipo": usuario.tipo,
        "congregacao_id": usuario.congregacao_id
    }), 200

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"mensagem": "Logout realizado com sucesso"}), 200