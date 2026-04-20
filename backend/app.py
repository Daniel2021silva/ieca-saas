import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database.db import db
import models
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["DATABASE_DIR"], exist_ok=True)

db.init_app(app)
CORS(app, supports_credentials=True)

app.register_blueprint(auth_bp, url_prefix="/api/auth")

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "mensagem": "Backend IECA funcionando"
    })

@app.route("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "backend": "flask",
        "database": "sqlite"
    })

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    print("iniciando backend...")
    app.run(host="127.0.0.1", port=5000, debug=True)