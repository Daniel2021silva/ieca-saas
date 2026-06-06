import os
from flask import Flask, send_from_directory

from database.db import db

from routes.auth_routes import auth_bp
from routes.posts_routes import posts_bp
from routes.congregacoes_routes import congregacoes_bp
from routes.secretaria_routes import secretaria_bp
from routes.financeiro_routes import financeiro_bp

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
DB_PATH = os.path.join(BASE_DIR, "database", "igreja.db")

app = Flask(
    __name__,
    static_folder=PROJECT_ROOT,
    static_url_path=""
)

app.config["SECRET_KEY"] = "ieca-chave-secreta-forte-troque-isso"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models import (
        Usuario,
        Congregacao,
        Departamento,
        Membro,
        Ocorrencia,
        Patrimonio,
        Post,
        LancamentoFinanceiro,
        Estudo
    )

    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(congregacoes_bp)
app.register_blueprint(secretaria_bp)
app.register_blueprint(financeiro_bp)


# =============================
# ROTAS DE PÁGINAS
# =============================
@app.get("/")
def home():
    return send_from_directory(PROJECT_ROOT, "index.html")


@app.get("/index.html")
def index_html():
    return send_from_directory(PROJECT_ROOT, "index.html")


@app.get("/feed.html")
def feed():
    return send_from_directory(PROJECT_ROOT, "feed.html")


@app.get("/register.html")
def register():
    return send_from_directory(PROJECT_ROOT, "register.html")


@app.get("/pages/<path:filename>")
def pages(filename):
    return send_from_directory(os.path.join(PROJECT_ROOT, "pages"), filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)