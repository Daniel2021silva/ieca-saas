async function login() {
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();

    if (!email || !senha) {
        alert("Preencha email e senha");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
            body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.erro || "Erro ao fazer login");
            return;
        }

        // salva dados básicos no storage só para o front usar
        storage.set("usuario", data.usuario);

        const context = {
            nome: data.usuario.nome,
            tipo: data.usuario.tipo,
            igreja: "IECA",
            congregacao_id: data.usuario.congregacao_id
        };

        storage.set("app_context", context);

        alert("Login realizado com sucesso!");
        window.location.href = "feed.html";

    } catch (error) {
        console.error("Erro no login:", error);
        alert("Não foi possível conectar ao backend.");
    }
}

async function logout() {
    try {
        await fetch("http://127.0.0.1:5000/api/auth/logout", {
            method: "POST",
            credentials: "include"
        });
    } catch (error) {
        console.error("Erro no logout:", error);
    }

    storage.set("usuario", null);
    storage.set("app_context", null);

    window.location.href = "../index.html";
}