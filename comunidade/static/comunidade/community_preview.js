"use strict";
// Muda o post para o modo edição
function setEditPost(element) {
    let postBody = element.querySelector(".post-body");
    let editPostBody = document.createElement("textarea");

    editPostBody.classList.add("post-body-edit");
    editPostBody.setAttribute("maxlength", "500");
    editPostBody.innerText = postBody.innerText;
    postBody.replaceWith(editPostBody);

    let botaoEditar = element.querySelector(".edit-post");
    let botaoSalvar = document.createElement("button");

    botaoSalvar.classList.add("post-save-edit");
    botaoSalvar.innerText = "Salvar";
    botaoSalvar.setAttribute("onclick", "editPost(this.parentNode)")
    botaoEditar.replaceWith(botaoSalvar);

    let botaoDeletar = element.querySelector(".delete-post");
    let botaoVoltar = document.createElement("button");

    botaoVoltar.classList.add("post-return-edit"); // Return???
    botaoVoltar.setAttribute("onclick", "setPost(this.parentNode)");
    botaoVoltar.innerText = "Voltar";
    botaoDeletar.replaceWith(botaoVoltar);
}

// Volta o post para o estado normal
function setPost(element) {
    let editPostBody = element.querySelector(".post-body-edit");
    let postBody = document.createElement("p");
    postBody.classList.add("post-body");
    postBody.innerText = editPostBody.innerHTML;
    editPostBody.replaceWith(postBody);

    let botaoSalvar = element.querySelector(".post-save-edit");
    let botaoEditar = document.createElement("button");
    botaoEditar.classList.add("edit-post");
    botaoEditar.setAttribute("onclick", "setEditPost(this.parentNode)");
    botaoEditar.innerText = "Editar";
    botaoSalvar.replaceWith(botaoEditar);

    let botaoVoltar = element.querySelector(".post-return-edit");
    let botaoDeletar = document.createElement("button");
    botaoDeletar.classList.add("delete-post");

    let aDeletar = document.createElement("a");
    aDeletar.setAttribute("href", "/comunidade/post/" + element.id + "/delete/");
    aDeletar.innerText = "Deletar";
    botaoDeletar.appendChild(aDeletar);

    botaoVoltar.replaceWith(botaoDeletar);

}

//Envia uma request para o server e caso receba uma response ele
//volta o post para o estado normal e insere o novo body(Texto do post)
async function editPost(element) {
    let editPostBody = element.querySelector(".post-body-edit")
    let body = editPostBody.value;
    let id = element.id;
    const response = await sendEditPost(body, id);

    editPostBody.innerHTML = response['postBody'];
    setPost(element);
}

//Envia uma request para o server com o id e o conteudo
//e retorna um status
async function sendEditPost(postBody, id) {
    const url = "/comunidade/post/edit/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'X-CSRFToken': getCookie("csrftoken") },
            body: JSON.stringify({
                "id": id,
                "postBody": postBody
            }),
        })
            .then(response => {
                console.log(response.status);
                if (!response.ok) {
                    throw new Error("HTTP STATUS " + response.status);
                }
                return response.json();
            })
            .then(response => {
                let result;
                result = response;
                return result;
            })
        return response;
    } catch (error) {
        console.error(error.message);
    }
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

async function like(element) {
    let likeElement = element.querySelector(".like-post");
    let curtidas = element.querySelector(".curtidas");
    let image = likeElement.querySelector(".like");
    let curtidasValue = parseInt(curtidas.innerText);

    await setLike(element.id);

    curtidasValue += 1;
    curtidas.innerText = curtidasValue;
    image.setAttribute("src", "/static/comunidade/dislike.png");
    likeElement.setAttribute("onclick", "dislike(this.parentNode)");
}

async function dislike(element) {
    let likeElement = element.querySelector(".like-post");
    let curtidas = element.querySelector(".curtidas");
    let image = likeElement.querySelector(".like");
    let curtidasValue = parseInt(curtidas.innerText);

    await setDislike(element.id);

    curtidasValue -= 1;
    curtidas.innerText = curtidasValue;
    image.setAttribute("src", "/static/comunidade/like.png");
    likeElement.setAttribute("onclick", "like(this.parentNode)");
}

async function setLike(id) {
    const url = "/comunidade/post/like/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'X-CSRFToken': getCookie("csrftoken") },
            body: JSON.stringify({
                "id": id
            }),
        })
            .then(response => {
                console.log(response.status);
                if (!response.ok) {
                    throw new Error("HTTP STATUS " + response.status);
                }
                return response.json();
            })
        return response;
    } catch (error) {
        console.error(error.message);
    }
}

async function setDislike(id) {
    const url = "/comunidade/post/dislike/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'X-CSRFToken': getCookie("csrftoken") },
            body: JSON.stringify({
                "id": id
            }),
        })
            .then(response => {
                console.log(response.status);
                if (!response.ok) {
                    throw new Error("HTTP STATUS " + response.status);
                }
                return response.json();
            })
        return response;
    } catch (error) {
        console.error(error.message);
    }
}
let musicaModal = document.getElementById("musica-modal");
let musicaModalContent = document.getElementById("modal-content");
let musicaBtn = document.getElementById("musica-btn");
let queryBtn = document.getElementById("query-btn");

musicaBtn.addEventListener("click", showMusicModal); //Botão para mostar modal
queryBtn.addEventListener("click", showMusicResults); // Pesquisa as musicas e mostra elas

window.onclick = function (event) { // Quando o modal está ativo
    if (event.target === musicaModal) { // Clicar em qualquer lugar fora dele
        musicaModal.style.display = "none"; // Fecha ele
    }
}
function showMusicModal() { // Mostra o modal da musica
    musicaModal.style.display = "block";
}

async function showMusicResults() {
    let musicName = document.getElementById("music-query").value;
    const response = await searchMusic(musicName);
    // Remove os botoes das musicas anteriores(caso existam)
    document.querySelectorAll('.musica-div').forEach(e => e.remove());

    let modalContentMusic = document.getElementById("modal-content-music");

    Object.entries(response).forEach(([key, val]) => {
        // Adiciona cada botão (quadrado) para músicas
        let musicaDiv = document.createElement("button");
        musicaDiv.setAttribute("type", "button");
        musicaDiv.className = "musica-div";

        let musicaNome = document.createElement("p");
        musicaNome.innerText = val["nome"];

        let musicaLink = document.createElement("p");
        musicaLink.innerText = val["linkmusica"];

        let musicaArtista = document.createElement("p");
        musicaArtista.innerText = val["nomeartista"];

        let musicaImagem = document.createElement("img");
        musicaImagem.setAttribute("src", val["imagem"]);
        musicaImagem.className = "musica-div";
        musicaImagem.style.width = "100px"; // da pra tirar isso daqui dps
        musicaImagem.style.height = "100px";

        modalContentMusic.appendChild(musicaDiv); //Adiciona uma das musicas para o modal
        musicaDiv.appendChild(musicaImagem) // Adiciona as caracteristicas da musicas para o modal
        musicaDiv.appendChild(musicaNome)
        musicaDiv.appendChild(musicaArtista);
        // Botão para selecionar músicas e mandar elas para o form  
        musicaDiv.setAttribute("onclick", `setMusic('${val["nome"]}','${val["nomeartista"]}','${val["linkmusica"]}','${val["imagem"]}')`);
    });
}

// Coloca os valores no form e fecha o modal
function setMusic(musicaNome, musicaArtista, musicaLink, musicaImagem) {
    document.getElementById("id_musica_nome").value = musicaNome;
    document.getElementById("id_musica_artista").value = musicaArtista;
    document.getElementById("id_musica_link").value = musicaLink;
    document.getElementById("id_musica_imagem").value = musicaImagem;
    musicaModal.style.display = "none";
}

// Pesquisa as musicas e retorna os primeiros 9 resultados
async function searchMusic(musicName) {
    const url = "/comunidade/musicas/";
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { 'X-CSRFToken': getCookie("csrftoken") },
            body: JSON.stringify({
                "query": musicName
            }),
        })
            .then(response => {
                console.log(response.status);
                if (!response.ok) {
                    throw new Error("HTTP STATUS " + response.status);
                }
                return response.json();
            })
            .then(data => {
                return data['musicas'];
            })
        return response;
    } catch (error) {
        console.error(error.message);
    }
}