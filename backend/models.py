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

    # admin, pastor, lider, secretaria, financeiro
    tipo = db.Column(db.String(50), nullable=False, default="membro")

    ativo = db.Column(db.Boolean, default=True)

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=True
    )

    departamento_id = db.Column(
        db.Integer,
        db.ForeignKey("departamentos.id"),
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

    departamento = db.relationship("Departamento", backref="usuarios", lazy=True)

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
            "congregacao_nome": self.congregacao.nome if self.congregacao else None,
            "departamento_id": self.departamento_id,
            "departamento_nome": self.departamento.nome if self.departamento else None,
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

    # 🔥 NOVO (responsáveis)
    responsavel_nome = db.Column(db.String(150), nullable=True)
    responsavel_funcao = db.Column(db.String(100), nullable=True)
    responsavel_whatsapp = db.Column(db.String(20), nullable=True)

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

    membros = db.relationship("Membro", backref="congregacao", lazy=True)
    ocorrencias = db.relationship("Ocorrencia", backref="congregacao", lazy=True)
    patrimonios = db.relationship("Patrimonio", backref="congregacao", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "endereco": self.endereco,
            "cidade": self.cidade,
            "pastor_nome": self.pastor_nome,
            "responsavel_nome": self.responsavel_nome,
            "responsavel_funcao": self.responsavel_funcao,
            "responsavel_whatsapp": self.responsavel_whatsapp,
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
            "congregacao_nome": self.congregacao.nome if self.congregacao else None
        }


# =============================
# MEMBROS
# =============================
class Membro(db.Model):
    __tablename__ = "membros"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(30))
    endereco = db.Column(db.String(255))
    cargo = db.Column(db.String(80))
    batismo = db.Column(db.String(20))
    entrada = db.Column(db.String(20))
    desligamento = db.Column(db.String(20))

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=False
    )

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "telefone": self.telefone,
            "cargo": self.cargo,
            "congregacao_nome": self.congregacao.nome if self.congregacao else None
        }


# =============================
# OCORRÊNCIAS
# =============================
class Ocorrencia(db.Model):
    __tablename__ = "ocorrencias"

    id = db.Column(db.Integer, primary_key=True)
    nome_membro = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="nao")

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=False
    )

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


# =============================
# PATRIMÔNIO
# =============================
class Patrimonio(db.Model):
    __tablename__ = "patrimonios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(100))
    quantidade = db.Column(db.Integer, default=1)

    congregacao_id = db.Column(
        db.Integer,
        db.ForeignKey("congregacoes.id"),
        nullable=False
    )


# =============================
# POSTS
# =============================
class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    conteudo = db.Column(db.Text, nullable=False)

    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    congregacao_id = db.Column(db.Integer, db.ForeignKey("congregacoes.id"))

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


# =============================
# FINANCEIRO
# =============================
class LancamentoFinanceiro(db.Model):
    __tablename__ = "lancamentos_financeiros"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(20))  # entrada / saida
    valor = db.Column(db.Float)

    congregacao_id = db.Column(db.Integer, db.ForeignKey("congregacoes.id"))
    criado_por = db.Column(db.Integer, db.ForeignKey("usuarios.id"))

    data_lancamento = db.Column(db.DateTime, default=datetime.utcnow)


# =============================
# ESTUDOS
# =============================
class Estudo(db.Model):
    __tablename__ = "estudos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    descricao = db.Column(db.Text)

    autor_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    congregacao_id = db.Column(db.Integer, db.ForeignKey("congregacoes.id"))