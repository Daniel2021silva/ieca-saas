from app import app
from database.db import db
from models import Usuario, Congregacao, Departamento


# =============================
# FUNÇÕES AUXILIARES
# =============================
def criar_usuario(nome, email, senha, tipo, congregacao_id, departamento_id=None):
    usuario = Usuario.query.filter_by(email=email).first()

    if usuario:
        print(f"⚠️ Usuário já existe: {email}")
        return usuario

    usuario = Usuario(
        nome=nome,
        email=email,
        tipo=tipo,
        congregacao_id=congregacao_id,
        departamento_id=departamento_id
    )
    usuario.set_senha(senha)

    db.session.add(usuario)
    db.session.commit()

    print(f"✅ Usuário criado: {nome} ({tipo})")
    return usuario


def criar_departamento(nome, lider_nome, congregacao_id):
    dep = Departamento.query.filter_by(nome=nome, congregacao_id=congregacao_id).first()

    if dep:
        print(f"⚠️ Departamento já existe: {nome}")
        return dep

    dep = Departamento(
        nome=nome,
        lider_nome=lider_nome,
        congregacao_id=congregacao_id
    )

    db.session.add(dep)
    db.session.commit()

    print(f"✅ Departamento criado: {nome}")
    return dep


def criar_congregacao(nome, endereco, cidade, pastor_nome, resp_nome, resp_funcao, resp_whats):
    c = Congregacao.query.filter_by(nome=nome).first()

    if c:
        print(f"⚠️ Congregação já existe: {nome}")
        return c

    c = Congregacao(
        nome=nome,
        endereco=endereco,
        cidade=cidade,
        pastor_nome=pastor_nome,
        responsavel_nome=resp_nome,
        responsavel_funcao=resp_funcao,
        responsavel_whatsapp=resp_whats
    )

    db.session.add(c)
    db.session.commit()

    print(f"✅ Congregação criada: {nome}")
    return c


# =============================
# SEED PRINCIPAL
# =============================
def seed():
    with app.app_context():

        print("🔄 Iniciando seed do banco...")

        # =============================
        # MATRIZ
        # =============================
        matriz = Congregacao.query.filter_by(nome="Matriz").first()

        if not matriz:
            matriz = Congregacao(
                nome="Matriz",
                endereco="Endereço da Matriz",
                cidade="Pelotas",
                pastor_nome="Pr. Moisés Amorim",
                responsavel_nome="Pr. Moisés Amorim",
                responsavel_funcao="Pastor Presidente",
                responsavel_whatsapp=""
            )
            db.session.add(matriz)
            db.session.commit()
            print("✅ Matriz criada")
        else:
            print("⚠️ Matriz já existe")

        # =============================
        # CONGREGAÇÕES
        # =============================
        criar_congregacao(
            "Jardim América", "", "", "",
            "Pra. Natalie Amorim", "Responsável Provisória", "53991269897"
        )

        criar_congregacao(
            "Pestano", "", "", "",
            "Miss. Iuri Rodrigues", "Missionário", "53992049249"
        )

        criar_congregacao(
            "Canguçu", "", "", "",
            "Pr. Zildomar", "Pastor", "53991958093"
        )

        criar_congregacao(
            "Getúlio Vargas", "", "", "",
            "Ev. Everton Falcão", "Evangelista", "53999892514"
        )

        criar_congregacao(
            "Pedro Osório", "", "", "",
            "Pr. Moisés Amorim", "Responsável Provisório", "53991868015"
        )

        criar_congregacao(
            "Missões Internacional", "", "", "",
            "", "", ""
        )

        # =============================
        # DEPARTAMENTOS (MATRIZ)
        # =============================
        dep_diaconato = criar_departamento("Diaconato", "PB David Ávila", matriz.id)
        criar_departamento("Coral", "Pra. Natalie Amorim", matriz.id)
        dep_infantil = criar_departamento("Infantil", "Vanessa Black", matriz.id)
        dep_jovens = criar_departamento("Jovens", "EV Everton / Cristieli", matriz.id)
        dep_homens = criar_departamento("Homens", "DC Samuel", matriz.id)
        criar_departamento("Mulheres", "Pra. Natalie Amorim", matriz.id)
        dep_missoes = criar_departamento("Missões", "Pr. Claudiomiro Pacheco", matriz.id)
        dep_intercessao = criar_departamento("Intercessão", "Miss Edi", matriz.id)

        # =============================
        # ADMINS
        # =============================
        criar_usuario("Pr. Moisés Amorim", "moises@ieca.local", "123456", "admin", matriz.id)
        criar_usuario("Pra. Natalie Amorim", "natalie@ieca.local", "123456", "admin", matriz.id)
        criar_usuario("Daniel Borges", "daniel@ieca.local", "123456", "admin", matriz.id)

        # =============================
        # LÍDERES
        # =============================
        criar_usuario("PB David Ávila", "david@ieca.local", "123456", "lider", matriz.id, dep_diaconato.id)
        criar_usuario("Vanessa Black", "vanessa@ieca.local", "123456", "lider", matriz.id, dep_infantil.id)
        criar_usuario("EV Everton", "everton@ieca.local", "123456", "lider", matriz.id, dep_jovens.id)
        criar_usuario("Cristieli", "cristieli@ieca.local", "123456", "lider", matriz.id, dep_jovens.id)
        criar_usuario("DC Samuel", "samuel@ieca.local", "123456", "lider", matriz.id, dep_homens.id)
        criar_usuario("Pr. Claudiomiro Pacheco", "claudiomiro@ieca.local", "123456", "lider", matriz.id, dep_missoes.id)
        criar_usuario("Miss Edi", "edi@ieca.local", "123456", "lider", matriz.id, dep_intercessao.id)

        # =============================
        # SECRETARIA / FINANCEIRO
        # =============================
        criar_usuario("Secretaria Matriz", "secretaria@ieca.local", "123456", "secretaria", matriz.id)
        criar_usuario("Financeiro Matriz", "financeiro@ieca.local", "123456", "financeiro", matriz.id)

        print("🚀 Seed finalizado com sucesso!")


if __name__ == "__main__":
    seed()