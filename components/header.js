// 📌 IMPORTS
import { getContext, setContext } from "../js/services/app.js";


// 🎨 RENDER HEADER
export function renderHeader() {

    const context = getContext();

    return `
        <header class="header">

            <div class="header-left">
                <h2>IECA</h2>
            </div>

            <div class="header-right">

                <!-- 🔽 DROPDOWN CONGREGAÇÕES -->
                <select id="trocarCongregacao">
                    <option value="Matriz">Matriz</option>
                    <option value="Centro">Centro</option>
                    <option value="Pestano">Pestano</option>
                    <option value="Dunas">Dunas</option>
                </select>

                <!-- 👤 USUÁRIO -->
                <span class="user">
                    ${context?.nome || "Usuário"}
                </span>

            </div>

        </header>
    `;
}


// ⚙️ ATIVAR FUNCIONAMENTO DO HEADER
export function initHeader() {

    const context = getContext();

    const select = document.getElementById("trocarCongregacao");

    if (!select) return;

    // 🎯 SETAR VALOR ATUAL
    select.value = context.congregacao;

    // 🔄 TROCAR CONGREGAÇÃO
    select.addEventListener("change", function () {

        const novoContext = {
            ...context,
            congregacao: this.value
        };

        setContext(novoContext);

        // 🔄 RECARREGAR SISTEMA
        location.reload();
    });
}