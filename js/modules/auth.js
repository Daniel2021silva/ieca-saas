import { supabase } from "../services/supabase.js";

function salvarSessao(profile) {
    localStorage.setItem("usuario", JSON.stringify(profile));

    localStorage.setItem("app_context", JSON.stringify({
        tipo: profile.tipo === "matriz_admin" ? "matriz" : "congregacao",
        nome: profile.nome,
        usuario_tipo: profile.tipo,
        congregacao_id: profile.congregacao_id,
        igreja_origem_id: profile.congregacao_id || "matriz",
        igreja_origem_nome: profile.congregacao_id ? `Congregação ${profile.congregacao_id}` : "Matriz",
        igreja_visualizada_id: profile.congregacao_id || "matriz",
        igreja_visualizada_nome: profile.congregacao_id ? `Congregação ${profile.congregacao_id}` : "Matriz"
    }));
}

export async function loginRequest(email, senha) {
    email = String(email || "").trim().toLowerCase();
    senha = String(senha || "").trim();

    const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password: senha
    });

    if (error) {
        throw new Error("Email ou senha inválidos.");
    }

    const user = data.user;

    const { data: profile, error: profileError } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", user.id)
        .single();

    if (profileError || !profile) {
        throw new Error("Perfil do usuário não encontrado.");
    }

    if (profile.ativo === false) {
        throw new Error("Usuário bloqueado.");
    }

    salvarSessao(profile);

    return {
        mensagem: "Login realizado com sucesso",
        usuario: profile
    };
}

export async function getUsuarioAtual() {
    const { data, error } = await supabase.auth.getUser();

    if (error || !data.user) {
        return null;
    }

    const { data: profile } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", data.user.id)
        .single();

    if (profile) {
        salvarSessao(profile);
    }

    return profile || null;
}

export async function logoutRequest() {
    await supabase.auth.signOut();

    localStorage.removeItem("usuario");
    localStorage.removeItem("app_context");

    window.location.href = "/index.html";
}