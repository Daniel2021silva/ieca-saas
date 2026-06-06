// =============================
// LISTAR POSTS
// =============================
export async function listarPosts() {
    const response = await fetch("/api/posts", {
        method: "GET",
        credentials: "include"
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.erro || "Erro ao listar posts.");
    }

    return Array.isArray(data) ? data : [];
}

// =============================
// CRIAR POST
// =============================
export async function criarPost(conteudo, departamento = null) {
    const response = await fetch("/api/posts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({
            titulo: "Publicação",
            conteudo,
            departamento
        })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.erro || "Erro ao criar post.");
    }

    return data.post;
}

// =============================
// USUÁRIO ATUAL
// =============================
export async function getUsuarioAtual() {
    const response = await fetch("/api/auth/me", {
        method: "GET",
        credentials: "include"
    });

    if (!response.ok) {
        return null;
    }

    const data = await response.json();
    return data.usuario || null;
}

// =============================
// LOGOUT
// =============================
export async function logoutRequest() {
    await fetch("/api/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    window.location.href = "/index.html";
}