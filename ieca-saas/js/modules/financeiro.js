import { storage } from "../services/storage.js";
import { getContext } from "../services/app.js";

// ➕ ADICIONAR
export function adicionarLancamento(dado){

    const context = getContext();

    storage.push("financeiro", {
        ...dado,
        congregacao: context.congregacao,
        data: new Date()
    });
}

// 📊 LISTAR
export function listarLancamentos(){

    const context = getContext();
    const dados = storage.get("financeiro");

    // 👑 MATRIZ VÊ TUDO
    if(context.tipo === "admin"){
        return dados;
    }

    // 🏠 CONGREGAÇÃO VÊ SÓ O SEU
    return dados.filter(d => 
        d.congregacao === context.congregacao
    );
}