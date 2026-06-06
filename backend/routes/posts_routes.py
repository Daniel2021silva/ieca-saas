from flask import Blueprint, request, jsonify, session
from models import Post, Usuario
from database.db import db
from middleware.auth_middleware import login_required

posts_bp = Blueprint("posts", __name__, url_prefix="/api/posts")


@posts_bp.route("/", methods=["GET"])
@posts_bp.route("", methods=["GET"])
def listar_posts():
    try:
        posts = Post.query.order_by(Post.criado_em.desc()).all()
        return jsonify([p.to_dict() for p in posts]), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar posts: {str(e)}"}), 500


@posts_bp.route("/", methods=["POST"])
@posts_bp.route("", methods=["POST"])
@login_required
def criar_post():
    try:
        data = request.get_json(silent=True) or {}

        conteudo = (data.get("conteudo") or "").strip()
        titulo = (data.get("titulo") or "").strip()
        departamento = (data.get("departamento") or "").strip() or None

        if not conteudo:
            return jsonify({"erro": "Conteúdo é obrigatório"}), 400

        usuario = db.session.get(Usuario, session["user_id"])
        if not usuario:
            return jsonify({"erro": "Usuário inválido"}), 401

        post = Post(
            titulo=titulo or "Publicação",
            conteudo=conteudo,
            autor_id=usuario.id,
            congregacao_id=usuario.congregacao_id,
            departamento=departamento
        )

        db.session.add(post)
        db.session.commit()

        return jsonify({
            "ok": True,
            "post": post.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar post: {str(e)}"}), 500