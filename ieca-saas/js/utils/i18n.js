const translations = {
    pt: {
        welcome: "Bem-vindo",
        login: "Entrar",
        logout: "Sair",
        post: "Publicar",
        feed: "Feed da Igreja"
    },
    en: {
        welcome: "Welcome",
        login: "Login",
        logout: "Logout",
        post: "Post",
        feed: "Church Feed"
    }
};

function t(key){
    const lang = localStorage.getItem("lang") || "pt";
    return translations[lang][key] || key;
}

function setLang(lang){
    localStorage.setItem("lang", lang);
    location.reload();
}