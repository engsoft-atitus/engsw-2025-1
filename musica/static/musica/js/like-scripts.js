// Element é a imagem e o src o atritbuto que tem o link
async function likeMusic(element, nome, artista) {
    element.src = "https://cdn.glitch.global/569e6e49-726e-46db-afe9-b43e2f0dcadf/love.png?v=1748992652286";
    element.removeAttribute("onclick"); // Remove o onclick para impedir que o usuario execute mais curtidas
    // enquanto o sistema não retorna a curtida
    await like(nome, artista);
    element.classList.remove("like-status");
    element.classList.add("dislike-status");
    // esse `` é tipo um f do python em uma string e usa ${} pra formatar, é importante que nas strings
    //tenham '' pro html reconhecer
    element.setAttribute("onclick", `dislikeMusic(this,'${nome}','${artista}')`);
}
async function dislikeMusic(element, nome, artista) {
    element.src = "https://cdn.glitch.global/569e6e49-726e-46db-afe9-b43e2f0dcadf/peace.png?v=1748992644854";
    element.removeAttribute("onclick");
    await dislike(nome, artista); // Não tem ainda dislikeMusic, tenta ver se tu conseguir fazer com base no like
    element.classList.remove("dislike-status");
    element.classList.add("like-status");
    element.setAttribute("onclick", `likeMusic(this,'${nome}','${artista}')`);
}

//Eu não entendo essa função
//Ela retorna um cookie
//Eu copiei da documentação do django para pegar o csrftoken
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            // Seilá django, tu que escreveu isso dai
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function like(nome, artista) {
    const url = 'playlist/curtidas/';
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'X-CSRFToken': getCookie("csrftoken") }, // precisa do token
            body: JSON.stringify({
                "nome": nome,
                "artista": artista
            })
        })
            .then(
                response => {
                    console.log(response.status);
                    if (!response.ok) {
                        throw Error("HTTP STATUS " + response.status);
                    }
                    return response.json();
                }
            )
    } catch (error) {
        console.error(error.message);
    }
}
async function dislike(nome, artista) {
    const url = 'playlist/descurtir/';
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'X-CSRFToken': getCookie("csrftoken") }, // precisa do token
            body: JSON.stringify({
                "nome": nome,
                "artista": artista
            })
        })
            .then(
                response => {
                    console.log(response.status);
                    if (!response.ok) {
                        throw Error("HTTP STATUS " + response.status);
                    }
                    return response.json();
                }
            )
        return;
    } catch (error) {
        console.error(error.message);
    }
}