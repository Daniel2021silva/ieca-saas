from functools import wraps
from flask import session, jsonify


def roles_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"erro": "Não autenticado"}), 401

            tipo = session.get("tipo")
            if tipo not in roles:
                return jsonify({"erro": "Sem permissão"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator