from flask import Blueprint, request, jsonify, session
from database.db import db
from models import Membro, Ocorrencia, Patrimonio, Usuario
from middleware.auth_middleware import login_required
from middleware.permissions import roles_required

secretaria_bp = Blueprint("secretaria", __name__, url_prefix="/api/secretaria")


def get_usuario_logado():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return db.session.get(Usuario, user_id)


# =============================
# MEMBROS
# =============================
@secretaria_bp.route("/membros", methods=["GET"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def listar_membros():
    try:
        usuario = get_usuario_logado()
        if not usuario:
            return jsonify({"erro": "Usuário inválido"}), 401

        query = Membro.query

        if usuario.tipo != "admin":
            query = query.filter_by(congregacao_id=usuario.congregacao_id)

        membros = query.order_by(Membro.nome.asc()).all()
        return jsonify([m.to_dict() for m in membros]), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao listar membros: {str(e)}"}), 500


@secretaria_bp.route("/membros", methods=["POST"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def criar_membro():
    try:
        usuario = get_usuario_logado()
        if not usuario:
            return jsonify({"erro": "Usuário inválido"}), 401

        data = request.get_json(silent=True) or {}

        nome = (data.get("nome") or "").strip()
        telefone = (data.get("telefone") or "").strip()
        endereco = (data.get("endereco") or "").strip()
        cargo = (data.get("cargo") or "Membro").strip()
        batismo = (data.get("batismo") or "").strip()
        entrada = (data.get("entrada") or "").strip()
        desligamento = (data.get("desligamento") or "").strip()

        if not nome:
            return jsonify({"erro": "Nome é obrigatório"}), 400

        congregacao_id = usuario.congregacao_id if usuario.tipo != "admin" else (data.get("congregacao_id") or usuario.congregacao_id)

        membro = Membro(
            nome=nome,
            telefone=telefone,
            endereco=endereco,
            cargo=cargo,
            batismo=batismo,
            entrada=entrada,
            desligamento=desligamento,
            congregacao_id=congregacao_id
        )

        db.session.add(membro)
        db.session.commit()

        return jsonify({"ok": True, "membro": membro.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar membro: {str(e)}"}), 500


@secretaria_bp.route("/membros/<int:membro_id>", methods=["PUT"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def atualizar_membro(membro_id):
    try:
        usuario = get_usuario_logado()
        membro = db.session.get(Membro, membro_id)

        if not usuario or not membro:
            return jsonify({"erro": "Membro não encontrado"}), 404

        if usuario.tipo != "admin" and membro.congregacao_id != usuario.congregacao_id:
            return jsonify({"erro": "Sem permissão"}), 403

        data = request.get_json(silent=True) or {}

        membro.nome = (data.get("nome") or membro.nome).strip()
        membro.telefone = (data.get("telefone") or "").strip()
        membro.endereco = (data.get("endereco") or "").strip()
        membro.cargo = (data.get("cargo") or "Membro").strip()
        membro.batismo = (data.get("batismo") or "").strip()
        membro.entrada = (data.get("entrada") or "").strip()
        membro.desligamento = (data.get("desligamento") or "").strip()

        db.session.commit()

        return jsonify({"ok": True, "membro": membro.to_dict()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar membro: {str(e)}"}), 500


@secretaria_bp.route("/membros/<int:membro_id>", methods=["DELETE"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def excluir_membro(membro_id):
    try:
        usuario = get_usuario_logado()
        membro = db.session.get(Membro, membro_id)

        if not usuario or not membro:
            return jsonify({"erro": "Membro não encontrado"}), 404

        if usuario.tipo != "admin" and membro.congregacao_id != usuario.congregacao_id:
            return jsonify({"erro": "Sem permissão"}), 403

        db.session.delete(membro)
        db.session.commit()

        return jsonify({"ok": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir membro: {str(e)}"}), 500


# =============================
# OCORRÊNCIAS
# =============================
@secretaria_bp.route("/ocorrencias", methods=["GET"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def listar_ocorrencias():
    try:
        usuario = get_usuario_logado()
        query = Ocorrencia.query

        if usuario.tipo != "admin":
            query = query.filter_by(congregacao_id=usuario.congregacao_id)

        ocorrencias = query.order_by(Ocorrencia.criado_em.desc()).all()
        return jsonify([o.to_dict() for o in ocorrencias]), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao listar ocorrências: {str(e)}"}), 500


@secretaria_bp.route("/ocorrencias", methods=["POST"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def criar_ocorrencia():
    try:
        usuario = get_usuario_logado()
        data = request.get_json(silent=True) or {}

        nome_membro = (data.get("nome_membro") or "").strip()
        descricao = (data.get("descricao") or "").strip()
        status = (data.get("status") or "nao").strip()

        if not nome_membro or not descricao:
            return jsonify({"erro": "Nome do membro e descrição são obrigatórios"}), 400

        ocorrencia = Ocorrencia(
            nome_membro=nome_membro,
            descricao=descricao,
            status=status,
            congregacao_id=usuario.congregacao_id
        )

        db.session.add(ocorrencia)
        db.session.commit()

        return jsonify({"ok": True, "ocorrencia": ocorrencia.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar ocorrência: {str(e)}"}), 500


@secretaria_bp.route("/ocorrencias/<int:ocorrencia_id>", methods=["DELETE"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def excluir_ocorrencia(ocorrencia_id):
    try:
        usuario = get_usuario_logado()
        ocorrencia = db.session.get(Ocorrencia, ocorrencia_id)

        if not usuario or not ocorrencia:
            return jsonify({"erro": "Ocorrência não encontrada"}), 404

        if usuario.tipo != "admin" and ocorrencia.congregacao_id != usuario.congregacao_id:
            return jsonify({"erro": "Sem permissão"}), 403

        db.session.delete(ocorrencia)
        db.session.commit()

        return jsonify({"ok": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir ocorrência: {str(e)}"}), 500


# =============================
# PATRIMÔNIO
# =============================
@secretaria_bp.route("/patrimonio", methods=["GET"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def listar_patrimonio():
    try:
        usuario = get_usuario_logado()
        query = Patrimonio.query

        if usuario.tipo != "admin":
            query = query.filter_by(congregacao_id=usuario.congregacao_id)

        itens = query.order_by(Patrimonio.nome.asc()).all()
        return jsonify([{
            "id": p.id,
            "nome": p.nome,
            "categoria": p.categoria,
            "quantidade": p.quantidade,
            "congregacao_id": p.congregacao_id,
            "congregacao_nome": p.congregacao.nome if p.congregacao else None
        } for p in itens]), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao listar patrimônio: {str(e)}"}), 500


@secretaria_bp.route("/patrimonio", methods=["POST"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def criar_patrimonio():
    try:
        usuario = get_usuario_logado()
        data = request.get_json(silent=True) or {}

        nome = (data.get("nome") or "").strip()
        categoria = (data.get("categoria") or "").strip()
        quantidade = int(data.get("quantidade") or 1)

        if not nome:
            return jsonify({"erro": "Nome do item é obrigatório"}), 400

        item = Patrimonio(
            nome=nome,
            categoria=categoria,
            quantidade=quantidade,
            congregacao_id=usuario.congregacao_id
        )

        db.session.add(item)
        db.session.commit()

        return jsonify({"ok": True, "patrimonio": {
            "id": item.id,
            "nome": item.nome,
            "categoria": item.categoria,
            "quantidade": item.quantidade,
            "congregacao_id": item.congregacao_id,
            "congregacao_nome": item.congregacao.nome if item.congregacao else None
        }}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao criar patrimônio: {str(e)}"}), 500


@secretaria_bp.route("/patrimonio/<int:item_id>", methods=["PUT"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def atualizar_patrimonio(item_id):
    try:
        usuario = get_usuario_logado()
        item = db.session.get(Patrimonio, item_id)

        if not usuario or not item:
            return jsonify({"erro": "Item não encontrado"}), 404

        if usuario.tipo != "admin" and item.congregacao_id != usuario.congregacao_id:
            return jsonify({"erro": "Sem permissão"}), 403

        data = request.get_json(silent=True) or {}

        nome = (data.get("nome") or "").strip()
        categoria = (data.get("categoria") or "").strip()
        quantidade = int(data.get("quantidade") or 1)

        if not nome:
            return jsonify({"erro": "Nome do item é obrigatório"}), 400

        item.nome = nome
        item.categoria = categoria
        item.quantidade = quantidade

        db.session.commit()

        return jsonify({"ok": True, "patrimonio": {
            "id": item.id,
            "nome": item.nome,
            "categoria": item.categoria,
            "quantidade": item.quantidade,
            "congregacao_id": item.congregacao_id,
            "congregacao_nome": item.congregacao.nome if item.congregacao else None
        }}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao atualizar patrimônio: {str(e)}"}), 500


@secretaria_bp.route("/patrimonio/<int:item_id>", methods=["DELETE"])
@login_required
@roles_required("admin", "pastor", "secretaria")
def excluir_patrimonio(item_id):
    try:
        usuario = get_usuario_logado()
        item = db.session.get(Patrimonio, item_id)

        if not usuario or not item:
            return jsonify({"erro": "Item não encontrado"}), 404

        if usuario.tipo != "admin" and item.congregacao_id != usuario.congregacao_id:
            return jsonify({"erro": "Sem permissão"}), 403

        db.session.delete(item)
        db.session.commit()

        return jsonify({"ok": True}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao excluir patrimônio: {str(e)}"}), 500