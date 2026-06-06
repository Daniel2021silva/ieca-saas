from flask import Blueprint, request, jsonify, session
from models import Usuario
from database.db import db
from middleware.auth_middleware import login_required

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# =============================
# LOGIN
# =============================
@auth_bp.post("/login")
def login():
    try:
        data = request.get_json(silent=True) or {}

        email = (data.get("email") or "").strip().lower()
        senha = data.get("senha") or ""

        if not email or not senha:
            return jsonify({"erro": "Email e senha são obrigatórios"}), 400

        usuario = Usuario.query.filter_by(email=email, ativo=True).first()

        if not usuario or not usuario.verificar_senha(senha):
            return jsonify({"erro": "Email ou senha inválidos"}), 401

        session.clear()
        session["user_id"] = usuario.id
        session["nome"] = usuario.nome
        session["email"] = usuario.email
        session["tipo"] = usuario.tipo
        session["congregacao_id"] = usuario.congregacao_id
        session["departamento_id"] = usuario.departamento_id

        return jsonify({
            "ok": True,
            "usuario": usuario.to_dict(),
            "redirect": "/feed.html"
        }), 200

    except Exception as e:
        return jsonify({"erro": f"Erro interno no login: {str(e)}"}), 500


# =============================
# USUÁRIO LOGADO
# =============================
@auth_bp.get("/me")
def me():
    try:
        if "user_id" not in session:
            return jsonify({"autenticado": False}), 401

        usuario = db.session.get(Usuario, session["user_id"])

        if not usuario:
            session.clear()
            return jsonify({"autenticado": False}), 401

        return jsonify({
            "autenticado": True,
            "usuario": usuario.to_dict()
        }), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao verificar sessão: {str(e)}"}), 500


# =============================
# LOGOUT
# =============================
@auth_bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True}), 200


# =============================
# ALTERAR A PRÓPRIA SENHA
# =============================
@auth_bp.post("/alterar-senha")
@login_required
def alterar_senha():
    try:
        usuario = db.session.get(Usuario, session["user_id"])

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        data = request.get_json(silent=True) or {}

        senha_atual = data.get("senha_atual") or ""
        nova_senha = data.get("nova_senha") or ""

        if not senha_atual or not nova_senha:
            return jsonify({"erro": "Informe a senha atual e a nova senha"}), 400

        if len(nova_senha) < 6:
            return jsonify({"erro": "A nova senha deve ter pelo menos 6 caracteres"}), 400

        if not usuario.verificar_senha(senha_atual):
            return jsonify({"erro": "Senha atual incorreta"}), 400

        usuario.set_senha(nova_senha)
        db.session.commit()

        return jsonify({"ok": True, "mensagem": "Senha alterada com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao alterar senha: {str(e)}"}), 500


# =============================
# LISTAR USUÁRIOS - ADMIN
# =============================
@auth_bp.get("/usuarios")
@login_required
def listar_usuarios():
    try:
        usuario_logado = db.session.get(Usuario, session["user_id"])

        if not usuario_logado or usuario_logado.tipo != "admin":
            return jsonify({"erro": "Sem permissão"}), 403

        usuarios = Usuario.query.order_by(Usuario.nome.asc()).all()

        return jsonify([u.to_dict() for u in usuarios]), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao listar usuários: {str(e)}"}), 500


# =============================
# CRIAR USUÁRIO - ADMIN
# =============================
@auth_bp.post("/usuarios")
@login_required
def criar_usuario():
    try:
        usuario_logado = db.session.get(Usuario, session["user_id"])

        if not usuario_logado or usuario_logado.tipo != "admin":
            return jsonify({"erro": "Sem permissão"}), 403

        data = request.get_json(silent=True) or {}

        nome = (data.get("nome") or "").strip()
        email = (data.get("email") or "").strip().lower()
        senha = data.get("senha") or ""
        tipo = (data.get("tipo") or "").strip()
        congregacao_id = data.get("congregacao_id")
        departamento_id = data.get("departamento_id")

        if not nome or not email or not senha or not tipo:
            return jsonify({"erro": "Nome, email, senha e tipo são obrigatórios"}), 400

        if len(senha) < 6:
            return jsonify({"erro": "A senha deve ter pelo menos 6 caracteres"}), 400

        if tipo not in ["admin", "pastor", "lider", "secretaria", "financeiro", "membro"]:
            return jsonify({"erro": "Tipo de usuário inválido"}), 400

        existente = Usuario.query.filter_by(email=email).first()
        if existente:
            return jsonify({"erro": "Já existe um usuário com este email"}), 400

        novo_usuario = Usuario(
            nome=nome,
            email=email,
            tipo=tipo,
            congregacao_id=congregacao_id,
            departamento_id=departamento_id,
            ativo=True
        )

        novo_usuario.set_senha(senha)

        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({
            "ok": True,
            "usuario": novo_usuario.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar usuário: {str(e)}"}), 500


# =============================
# RESETAR SENHA DE USUÁRIO - ADMIN
# =============================
@auth_bp.put("/usuarios/<int:user_id>/resetar-senha")
@login_required
def resetar_senha(user_id):
    try:
        usuario_logado = db.session.get(Usuario, session["user_id"])

        if not usuario_logado or usuario_logado.tipo != "admin":
            return jsonify({"erro": "Sem permissão"}), 403

        usuario = db.session.get(Usuario, user_id)

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        data = request.get_json(silent=True) or {}
        nova_senha = data.get("nova_senha") or ""

        if len(nova_senha) < 6:
            return jsonify({"erro": "A nova senha deve ter pelo menos 6 caracteres"}), 400

        usuario.set_senha(nova_senha)
        db.session.commit()

        return jsonify({"ok": True, "mensagem": "Senha redefinida com sucesso"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao redefinir senha: {str(e)}"}), 500


# =============================
# ATIVAR / DESATIVAR USUÁRIO - ADMIN
# =============================
@auth_bp.put("/usuarios/<int:user_id>/status")
@login_required
def alterar_status_usuario(user_id):
    try:
        usuario_logado = db.session.get(Usuario, session["user_id"])

        if not usuario_logado or usuario_logado.tipo != "admin":
            return jsonify({"erro": "Sem permissão"}), 403

        usuario = db.session.get(Usuario, user_id)

        if not usuario:
            return jsonify({"erro": "Usuário não encontrado"}), 404

        data = request.get_json(silent=True) or {}
        ativo = data.get("ativo")

        if ativo is None:
            return jsonify({"erro": "Informe o status ativo"}), 400

        usuario.ativo = bool(ativo)
        db.session.commit()

        return jsonify({
            "ok": True,
            "usuario": usuario.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao alterar status: {str(e)}"}), 500