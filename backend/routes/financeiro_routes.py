from flask import Blueprint, request, jsonify, session
from database.db import db
from models import LancamentoFinanceiro, Usuario
from middleware.auth_middleware import login_required
from middleware.permissions import roles_required

financeiro_bp = Blueprint("financeiro", __name__, url_prefix="/api/financeiro")


def get_usuario_logado():
    user_id = session.get("user_id")
    if not user_id: