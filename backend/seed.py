from app import app
from database.db import db
from models import Usuario, Congregacao, Departamento


def seed():
    with app.app_context():

        print("🔄 Iniciando seed do banco...")

        # =============================
        # VERIFICA SE JÁ EXISTE ADMIN
        # =============================
        if Usuario.query.filter_by(email="admin@igreja.com").first():
            print("⚠️ Seed já executado. Admin já existe.")
            return

        # =============================
        # CRIA MATRIZ
        # =============================
        matriz = Congregacao(
            nome="Matriz",
            endereco="Endereço da Matriz",
            cidade="Pelotas",
            pastor_nome="Pr. Moisés Amorim"
        )
        db.session.add(matriz)
        db.session.commit()

        print("✅ Matriz criada")

        # =============================
        # CRIA ADMIN
        # =============================
        admin = Usuario(
            nome="Administrador Geral",
            email="admin@igreja.com",
            tipo="admin",
            congregacao_id=matriz.id
        )
        admin.set_senha("123456")

        db.session.add(admin)
        db.session.commit()

        print("✅ Admin criado")
        print("📧 Email: admin@igreja.com")
        print("🔑 Senha: 123456")

        # =============================
        # DEPARTAMENTOS PADRÃO
        # =============================
        departamentos = [
            "Diaconato",
            "Coral",
            "Infantil",
            "Jovens",
            "Homens",
            "Mulheres",
            "Missões",
            "Intercessão",
            "Social",
            "Estudos"
        ]

        for nome_dep in departamentos:
            dep = Departamento(
                nome=nome_dep,
                lider_nome="",
                congregacao_id=matriz.id
            )
            db.session.add(dep)

        db.session.commit()

        print("✅ Departamentos criados")

        # =============================
        # CRIAR CONGREGAÇÕES EXEMPLO
        # =============================
        congregacoes = [
            "Jardim América",
            "Pestano",
            "Canguçu",
            "Getúlio Vargas",
            "Pedro Osório",
            "Missões Internacional"
        ]

        for nome in congregacoes:
            c = Congregacao(
                nome=nome,
                endereco="",
                cidade="",
                pastor_nome=""
            )
            db.session.add(c)

        db.session.commit()

        print("✅ Congregações criadas")

        print("🚀 Seed finalizado com sucesso!")


if __name__ == "__main__":
    seed()