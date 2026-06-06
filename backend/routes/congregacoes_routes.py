from flask import Blueprint, jsonify
from models import Congregacao

congregacoes_bp = Blueprint("congregacoes", __name__, url_prefix="/api/congregacoes")


@congregacoes_bp.route("/", methods=["GET"])
@congregacoes_bp.route("", methods=["GET"])
def listar_congregacoes():
    try:
        congregacoes = Congregacao.query.order_by(Congregacao.nome.asc()).all()
        return jsonify([c.to_dict() for c in congregacoes]), 200
    except Exception as e:
        return jsonify({"erro": f"Erro ao listar congregações: {str(e)}"}), 500