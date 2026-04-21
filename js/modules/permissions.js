// 🔐 PEGAR USUÁRIO LOGADO
function getUser(){
    return JSON.parse(localStorage.getItem("ieca_user"));
}

// 🔒 PROTEGER PÁGINAS (LOGIN OBRIGATÓRIO)
function protegerPagina(){

    const usuario = getUser();

    if(!usuario){
        alert("Acesso restrito. Faça login.");
        window.location.href = "../index.html";
        return false;
    }

    return true;
}

// 🎯 PERMISSÕES

// Pode postar?
function podePostar(){
    const user = getUser();
    return user && (user.tipo === "membro" || user.tipo === "lider" || user.tipo === "admin");
}

// Pode comentar?
function podeComentar(){
    return true; // todos podem
}

// Pode curtir?
function podeCurtir(){
    return true;
}

// Apenas admin
function isAdmin(){
    const user = getUser();
    return user && user.tipo === "admin";
}

// Líder ou admin
function isLider(){
    const user = getUser();
    return user && (user.tipo === "lider" || user.tipo === "admin");
}

// 🔥 AUTO EXECUÇÃO (SÓ BLOQUEIA PÁGINAS INTERNAS)
(function(){

    const paginaPublica = window.location.pathname.includes("feed.html");

    if(paginaPublica) return;

    protegerPagina();

})();