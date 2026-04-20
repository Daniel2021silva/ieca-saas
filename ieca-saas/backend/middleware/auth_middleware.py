from functools import wraps
from flask import session, jsonify


# =============================
# LOGIN OBRIGATÓRIO
# =============================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "usuario_id" not in session:
            return jsonify({
                "erro": "Não autenticado"
            }), 401

        return f(*args, **kwargs)

    return decorated_function


# =============================
# VERIFICA TIPO DE USUÁRIO
# =============================
def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if "usuario_tipo" not in session:
                return jsonify({
                    "erro": "Não autenticado"
                }), 401

            if session["usuario_tipo"] not in roles:
                return jsonify({
                    "erro": "Sem permissão"
                }), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator


# =============================
# DADOS DO USUÁRIO ATUAL
# =============================
def get_current_user():
    return {
        "id": session.get("usuario_id"),
        "nome": session.get("usuario_nome"),
        "tipo": session.get("usuario_tipo"),
        "congregacao_id": session.get("congregacao_id")
    }