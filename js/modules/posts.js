const KEY_POSTS = "ieca_posts";

// 🔐 PEGAR USUÁRIO
function getUser(){
    return JSON.parse(localStorage.getItem("ieca_user"));
}

// 🔥 CRIAR POST
function criarPost(){

    const user = getUser();

    if(!user){
        alert("Faça login para postar");
        return;
    }

    // 🔒 PERMISSÃO
    if(!(user.tipo === "membro" || user.tipo === "lider" || user.tipo === "admin")){
        alert("Você não tem permissão para postar");
        return;
    }

    const texto = document.getElementById("texto").value;
    const fileInput = document.getElementById("midia");
    const file = fileInput.files[0];

    if(!texto && !file){
        alert("Escreva algo ou selecione uma mídia");
        return;
    }

    // 🔥 DEPARTAMENTO ATUAL
    const departamentoAtual = localStorage.getItem("departamento_ativo") || "geral";

    const reader = new FileReader();

    reader.onload = function(e){

        const posts = JSON.parse(localStorage.getItem(KEY_POSTS)) || [];

        posts.push({
            id: Date.now(),
            autor: user.nome || "Membro",
            texto: texto,
            midia: file ? e.target.result : null,
            tipo: file ? file.type : null,
            departamento: departamentoAtual, // 🔥 NOVO
            likes: 0,
            comentarios: []
        });

        localStorage.setItem(KEY_POSTS, JSON.stringify(posts));

        document.getElementById("texto").value = "";
        fileInput.value = "";

        listarPosts();
    };

    if(file){
        reader.readAsDataURL(file);
    } else {
        reader.onload({ target: { result: null } });
    }
}

// 🔥 LISTAR POSTS
function listarPosts(){

    const feed = document.getElementById("feed");
    if(!feed) return;

    const posts = JSON.parse(localStorage.getItem(KEY_POSTS)) || [];

    const depAtual = localStorage.getItem("departamento_ativo") || "geral";

    feed.innerHTML = "";

    posts
    .filter(post => depAtual === "geral" || post.departamento === depAtual)
    .slice()
    .reverse()
    .forEach(post => {

        let midiaHTML = "";

        if(post.tipo && post.tipo.startsWith("image")){
            midiaHTML = `<img src="${post.midia}" class="post-img">`;
        }

        if(post.tipo && post.tipo.startsWith("video")){
            midiaHTML = `
                <video controls class="post-img">
                    <source src="${post.midia}">
                </video>
            `;
        }

        const div = document.createElement("div");
        div.className = "post";

        div.innerHTML = `
            <div class="post-header">
                <div class="avatar">${post.autor.charAt(0)}</div>
                <strong>${post.autor}</strong>
                <small style="margin-left:auto;">${post.departamento}</small>
            </div>

            <p class="post-text">${post.texto}</p>

            ${midiaHTML}

            <div class="post-actions">
                <button onclick="curtir(${post.id})">❤️ ${post.likes}</button>
                <button onclick="toggleComentarios(${post.id})">💬 ${post.comentarios.length}</button>
            </div>

            <div id="comentarios-${post.id}" class="comentarios" style="display:none;">
                ${post.comentarios.map(c => `
                    <p><strong>${c.nome}:</strong> ${c.texto}</p>
                `).join("")}

                <input type="text" id="input-${post.id}" placeholder="Comentar... 😊🔥❤️">
                <button onclick="comentar(${post.id})">Enviar</button>
            </div>
        `;

        feed.appendChild(div);
    });
}

// 🔥 CURTIR
function curtir(id){
    const posts = JSON.parse(localStorage.getItem(KEY_POSTS));
    const post = posts.find(p => p.id === id);

    post.likes++;

    localStorage.setItem(KEY_POSTS, JSON.stringify(posts));
    listarPosts();
}

// 🔥 COMENTÁRIOS
function toggleComentarios(id){
    const el = document.getElementById(`comentarios-${id}`);
    el.style.display = el.style.display === "none" ? "block" : "none";
}

function comentar(id){

    const user = getUser();
    const input = document.getElementById(`input-${id}`);
    const texto = input.value.trim();

    if(!texto) return;

    const posts = JSON.parse(localStorage.getItem(KEY_POSTS));
    const post = posts.find(p => p.id === id);

    post.comentarios.push({
        nome: user ? user.nome : "Visitante",
        texto
    });

    localStorage.setItem(KEY_POSTS, JSON.stringify(posts));

    listarPosts();
}

// 🔥 INICIALIZAÇÃO
window.onload = function(){
    listarPosts();
};