import os

# =============================
# BASE DO PROJETO
# =============================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =============================
# PASTA DO BANCO
# =============================
DATABASE_DIR = os.path.join(BASE_DIR, "database")

# Caminho do arquivo SQLite
DATABASE_PATH = os.path.join(DATABASE_DIR, "igreja.db")


# =============================
# CONFIG PRINCIPAL
# =============================
class Config:
    # Segurança
    SECRET_KEY = "troque-essa-chave-em-producao"

    # Banco de dados
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JSON (aceitar acentos normalmente)
    JSON_AS_ASCII = False

    # Pasta do banco (usada no app.py)
    DATABASE_DIR = DATABASE_DIR

    # Debug
    DEBUG = True


# =============================
# CONFIG PRODUÇÃO (FUTURO)
# =============================
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-super-segura")