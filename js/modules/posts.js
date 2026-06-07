import { supabase } from "../services/supabase.js";
import { getUsuarioAtual, logoutRequest } from "./auth.js";

// =============================
// LISTAR POSTS - SUPABASE
// =============================
export async function listarPosts() {
    const { data, error } = await supabase
        .from("posts")
        .select(`
            id,
            conteudo,
            created_at,
            congregacao_id
        `)
        .order("created_at", { ascending: false });

    if (error) {
        throw new Error(error.message || "Erro ao listar posts.");
    }

    return (data || []).map(post => ({
        id: post.id,
        conteudo: post.conteudo,
        criado_em: post.created_at,
        congregacao_nome: post.congregacao_id
            ? `Congregação ${post.congregacao_id}`
            : "IECA",
        autor_nome: "IECA"
    }));
}

// =============================
// CRIAR POST - SUPABASE
// =============================
export async function criarPost(conteudo, departamento = null) {
    const usuario = await getUsuarioAtual();

    if (!usuario) {
        throw new Error("Usuário não autenticado.");
    }

    const novoPost = {
        conteudo: conteudo,
        congregacao_id: usuario.congregacao_id || null
    };

    const { data, error } = await supabase
        .from("posts")
        .insert([novoPost])
        .select()
        .single();

    if (error) {
        throw new Error(error.message || "Erro ao criar post.");
    }

    return data;
}

export { getUsuarioAtual, logoutRequest };