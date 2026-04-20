const storage = {

    get(key, defaultValue = null){
        try{
            const raw = localStorage.getItem(key);

            if(raw === null || raw === undefined){
                return defaultValue;
            }

            return JSON.parse(raw);
        }catch(error){
            console.error("Erro ao ler storage:", key, error);
            return defaultValue;
        }
    },

    set(key, data){
        try{
            localStorage.setItem(key, JSON.stringify(data));
        }catch(error){
            console.error("Erro ao salvar storage:", key, error);
        }
    },

    push(key, item){
        let data = this.get(key, []);

        if(!Array.isArray(data)){
            data = [];
        }

        data.push(item);
        this.set(key, data);
    },

    remove(key){
        localStorage.removeItem(key);
    },

    clear(){
        localStorage.clear();
    }
};

// TORNA GLOBAL
window.storage = storage;