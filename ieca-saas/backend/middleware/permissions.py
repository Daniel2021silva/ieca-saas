# =============================
# TIPOS DE USUÁRIO
# =============================
ROLE_ADMIN = "admin"
ROLE_PASTOR = "pastor"
ROLE_LIDER = "lider"
ROLE_SECRETARIA = "secretaria"
ROLE_FINANCEIRO = "financeiro"
ROLE_MEMBRO = "membro"


# =============================
# PERMISSÕES POR MÓDULO
# =============================
PERMISSIONS = {
    "usuarios": [ROLE_ADMIN],
    "congregacoes": [ROLE_ADMIN, ROLE_PASTOR],
    "departamentos": [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER],
    "posts": [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER, ROLE_SECRETARIA],
    "financeiro": [ROLE_ADMIN, ROLE_PASTOR, ROLE_FINANCEIRO],
    "estudos": [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER, ROLE_SECRETARIA],
    "secretaria": [ROLE_ADMIN, ROLE_PASTOR, ROLE_SECRETARIA],
    "dashboard": [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER, ROLE_SECRETARIA, ROLE_FINANCEIRO, ROLE_MEMBRO],
}


# =============================
# VERIFICA SE A ROLE EXISTE
# =============================
def is_valid_role(role):
    return role in {
        ROLE_ADMIN,
        ROLE_PASTOR,
        ROLE_LIDER,
        ROLE_SECRETARIA,
        ROLE_FINANCEIRO,
        ROLE_MEMBRO,
    }


# =============================
# RETORNA PERMISSÕES DE UM MÓDULO
# =============================
def get_module_roles(module_name):
    return PERMISSIONS.get(module_name, [])


# =============================
# VERIFICA SE A ROLE TEM ACESSO AO MÓDULO
# =============================
def has_module_access(role, module_name):
    allowed_roles = get_module_roles(module_name)
    return role in allowed_roles


# =============================
# VERIFICA SE PODE CRIAR USUÁRIOS
# =============================
def can_create_user(role):
    return role == ROLE_ADMIN


# =============================
# VERIFICA SE PODE GERENCIAR CONGREGAÇÕES
# =============================
def can_manage_congregacoes(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR]


# =============================
# VERIFICA SE PODE GERENCIAR DEPARTAMENTOS
# =============================
def can_manage_departamentos(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER]


# =============================
# VERIFICA SE PODE PUBLICAR POSTS
# =============================
def can_create_post(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER, ROLE_SECRETARIA]


# =============================
# VERIFICA SE PODE VER POSTS
# =============================
def can_view_posts(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER, ROLE_SECRETARIA, ROLE_FINANCEIRO, ROLE_MEMBRO]


# =============================
# VERIFICA SE PODE USAR O FINANCEIRO
# =============================
def can_manage_financeiro(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR, ROLE_FINANCEIRO]


# =============================
# VERIFICA SE PODE GERENCIAR ESTUDOS
# =============================
def can_manage_estudos(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR, ROLE_LIDER, ROLE_SECRETARIA]


# =============================
# VERIFICA SE PODE ACESSAR SECRETARIA
# =============================
def can_manage_secretaria(role):
    return role in [ROLE_ADMIN, ROLE_PASTOR, ROLE_SECRETARIA]


# =============================
# VERIFICA SE PODE ACESSAR DASHBOARD
# =============================
def can_access_dashboard(role):
    return role in [
        ROLE_ADMIN,
        ROLE_PASTOR,
        ROLE_LIDER,
        ROLE_SECRETARIA,
        ROLE_FINANCEIRO,
        ROLE_MEMBRO
    ]