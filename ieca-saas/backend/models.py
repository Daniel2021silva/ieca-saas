from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db


# =============================
# USUÁRIOS
# =============================
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)

    # admin, pastor, lider, secretaria, financeiro, membro
    tipo = db.Column(db.String(50), nullable=False, default="membro")

    ativo = db.Column(db.Boolean, default=True)

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=True
    )

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    posts = db.relationship("Post", backref="autor", lazy=True)
    lancamentos = db.relationship("LancamentoFinanceiro", backref="usuario", lazy=True)
    estudos = db.relationship("Estudo", backref="autor", lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "tipo": self.tipo,
            "ativo": self.ativo,
            "congregacao_id": self.congregacao_id,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }


# =============================
# CONGREGAÇÕES
# =============================
class Congregacao(db.Model):
    __tablename__ = "congregacoes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    endereco = db.Column(db.String(255), nullable=True)
    cidade = db.Column(db.String(120), nullable=True)
    pastor_nome = db.Column(db.String(120), nullable=True)
    ativa = db.Column(db.Boolean, default=True)

    criada_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizada_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    usuarios = db.relationship("Usuario", backref="congregacao", lazy=True)
    departamentos = db.relationship("Departamento", backref="congregacao", lazy=True)
    posts = db.relationship("Post", backref="congregacao", lazy=True)
    lancamentos = db.relationship("LancamentoFinanceiro", backref="congregacao", lazy=True)
    estudos = db.relationship("Estudo", backref="congregacao", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "pastor_nome": self.pastor_nome,
            "ativa": self.ativa,
            "criada_em": self.criada_em.isoformat() if self.criada_em else None,
            "atualizada_em": self.atualizada_em.isoformat() if self.atualizada_em else None
        }


# =============================
# DEPARTAMENTOS
# =============================
class Departamento(db.Model):
    __tablename__ = "departamentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    lider_nome = db.Column(db.String(120), nullable=True)
    ativo = db.Column(db.Boolean, default=True)

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=False
    )

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao,
            "lider_nome": self.lider_nome,
            "ativo": self.ativo,
            "congregacao_id": self.congregacao_id,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }


# =============================
# POSTS / FEED
# =============================
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    conteudo = db.Column(db.Text, nullable=False)

    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=True
    )

    departamento = db.Column(db.String(120), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "conteudo": self.conteudo,
            "autor_id": self.autor_id,
            "autor_nome": self.autor.nome if self.autor else None,
            "congregacao_id": self.congregacao_id,
            "congregacao_nome": self.congregacao.nome if self.congregacao else None,
            "departamento": self.departamento,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }


# =============================
# FINANCEIRO
# =============================
class LancamentoFinanceiro(db.Model):
    __tablename__ = "lancamentos_financeiros"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150), nullable=False)

    # entrada | saida
    tipo = db.Column(db.String(20), nullable=False)

    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(100), nullable=True)

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=True
    )

    criado_por = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    data_lancamento = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "valor": self.valor,
            "categoria": self.categoria,
            "congregacao_id": self.congregacao_id,
            "congregacao_nome": self.congregacao.nome if self.congregacao else None,
            "criado_por": self.criado_por,
            "criado_por_nome": self.usuario.nome if self.usuario else None,
            "data_lancamento": self.data_lancamento.isoformat() if self.data_lancamento else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }


# =============================
# ESTUDOS
# =============================
class Estudo(db.Model):
    __tablename__ = "estudos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    # pdf, video, link, texto
    tipo = db.Column(db.String(50), nullable=False, default="texto")

    conteudo = db.Column(db.Text, nullable=True)
    link = db.Column(db.String(255), nullable=True)

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=True
    )

    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "tipo": self.tipo,
            "conteudo": self.conteudo,
            "link": self.link,
            "congregacao_id": self.congregacao_id,
            "congregacao_nome": self.congregacao.nome if self.congregacao else None,
            "autor_id": self.autor_id,
            "autor_nome": self.autor.nome if self.autor else None,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }