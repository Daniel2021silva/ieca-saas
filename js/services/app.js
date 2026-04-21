// =============================
// 📌 CONTEXTO GLOBAL
// =============================
const DEV_MODE = true;

// 🔥 ALTERE AQUI PARA TESTAR
const DEV_USER = {
    nome: "Daniel",
    tipo: "admin", // admin | secretaria | tesoureiro | pastor
    igreja: "IECA",
    congregacao: "IECA - IGREJA EVANGÉLICA CONGREGAÇÃO DO AVIVAMENTO (MATRIZ)"
};

export function getContext() {
    return JSON.parse(localStorage.getItem("app_context")) || null;
}

export function setContext(context) {
    localStorage.setItem("app_context", JSON.stringify(context));
}


// =============================
// 👤 USUÁRIO
// =============================
export function getUser() {
    return JSON.parse(localStorage.getItem("usuario")) || null;
}

export function setUser(user) {
    localStorage.setItem("usuario", JSON.stringify(user));
}


// =============================
// 📦 STORAGE PADRÃO
// =============================
export function getStorage(key) {
    return JSON.parse(localStorage.getItem(key)) || [];
}

export function setStorage(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}


// =============================
// 🔐 PERMISSÕES (CORRIGIDO)
// =============================

export function isAdmin() {
    return getUser()?.tipo === "admin";
}

export function isSecretaria() {
    return getUser()?.tipo === "secretaria";
}

export function isTesoureiro() {
    return getUser()?.tipo === "tesoureiro";
}

export function isMatriz() {
    const nome = getContext()?.congregacao || "";
    return nome.toUpperCase().includes("MATRIZ");
}

// 👑 MATRIZ ADMIN vê tudo
export function podeVerTudo() {
    return isAdmin() && isMatriz();
}


// =============================
// 🔍 FILTRO POR CONGREGAÇÃO
// =============================

export function filtrarPorCongregacao(lista) {

    if (podeVerTudo()) return lista;

    const congregacao = getContext()?.congregacao;

    return lista.filter(item =>
        item.congregacao === congregacao
    );
}


// =============================
// 🔒 PROTEÇÃO DE ROTA
// =============================

export function protegerPagina(tiposPermitidos = []) {

    if (DEV_MODE) return true; // 🔥 LIBERA TUDO EM TESTE

    const user = getUser();

    if (!user) {
        redirecionarLogin();
        return false;
    }

    if (tiposPermitidos.length > 0 && !tiposPermitidos.includes(user.tipo)) {
        alert("Acesso negado");
        window.location.href = "../feed.html";
        return false;
    }

    return true;
}

function redirecionarLogin() {
    const isPage = window.location.pathname.includes("/pages/");
    window.location.href = isPage ? "../index.html" : "index.html";
}


// =============================
// 🔁 TROCAR CONGREGAÇÃO (MATRIZ)
// =============================

export function trocarCongregacao(nome) {

    let context = getContext();

    context.congregacao = nome;

    setContext(context);

    window.location.reload();
}


// =============================
// 🔙 VOLTAR PARA MATRIZ
// =============================

export function voltarMatriz() {

    let context = getContext();

    context.congregacao = getUser().congregacao;

    setContext(context);

    window.location.reload();
}


// =============================
// 🏗️ SEED INICIAL
// =============================

function seedCongregacoes() {

    let congregacoes = getStorage("congregacoes");

    if (congregacoes.length > 0) return;

    setStorage("congregacoes", [

        {
            nome: "IECA - IGREJA EVANGÉLICA CONGREGAÇÃO DO AVIVAMENTO (MATRIZ)",
            endereco: "Sede",
            cultos: "Cultos gerais"
        },

        {
            nome: "Jardim América",
            endereco: "Rua Olavo C Vergara 244",
            cultos: "Terça às 20h"
        },

        {
            nome: "Pestano",
            endereco: "Osmar Grafulha 183",
            cultos: "Terça e quinta às 20h"
        }

    ]);
}


// =============================
// 🚀 INIT GLOBAL
// =============================

window.onload = function () {

    let user = getUser();

    // 🔥 DEV MODE INTELIGENTE
    if (DEV_MODE) {
        user = DEV_USER;
        setUser(user);
    }

    // 🔐 PROTEÇÃO (SÓ FORA DO DEV)
    if (!user && !DEV_MODE) {
        redirecionarLogin();
        return;
    }

    // 🔥 CONTEXTO CONSISTENTE
    let context = getContext();

    if (!context || !context.usuario) {

        context = {
            usuario: user,
            congregacao: user.congregacao
        };

        setContext(context);
    }

    // 🏗️ SEED
    seedCongregacoes();

    // 🧪 DEBUG
    console.log("Modo DEV:", DEV_MODE);
    console.log("Usuário:", user);
    console.log("Contexto:", context);
};