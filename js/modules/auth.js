export async function loginRequest(email, senha) {
    const response = await fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify({ email, senha })
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.erro || "Falha no login");
    }

    return data;
}

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

export async function logoutRequest() {
    await fetch("/api/auth/logout", {
        method: "POST",
        credentials: "include"
    });

    window.location.href = "/index.html";
}