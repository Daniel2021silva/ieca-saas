// js/modules/permissoes.js

function getUser(){
    return JSON.parse(localStorage.getItem("usuario"));
}

function protegerPagina(){
    const usuario = getUser();

    if(!usuario){
        alert("Acesso restrito. Faça login.");
        window.location.href = "../index.html";
        return false;
    }

    return true;
}

function temTipo(...tiposPermitidos){
    const usuario = getUser();
    return usuario && tiposPermitidos.includes(usuario.tipo);
}

function exigirPermissao(...tiposPermitidos){
    if(!protegerPagina()) return false;

    if(!temTipo(...tiposPermitidos)){
        alert("Você não tem permissão para acessar esta área.");
        window.location.href = "../feed.html";
        return false;
    }

    return true;
}

function podePostar(){
    return temTipo("matriz_admin", "pastor", "secretaria", "departamento");
}

function podeAcessarFinanceiro(){
    return temTipo("matriz_admin", "financeiro");
}

function podeAcessarSecretaria(){
    return temTipo("matriz_admin", "secretaria", "pastor");
}

function podeAcessarDepartamentos(){
    return temTipo("matriz_admin", "departamento", "pastor");
}

function podeGerenciarUsuarios(){
    return temTipo("matriz_admin");
}

function isAdmin(){
    return temTipo("matriz_admin");
}

function logoutLocal(){
    localStorage.removeItem("usuario");
    localStorage.removeItem("app_context");
    window.location.href = "../index.html";
}