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
function editPost(element) {
    let editPostBody = element.querySelector(".post-body-edit")
    let body = editPostBody.value;
    let id = element.id;
    sendEditPost(body, id);
    editPostBody.innerHTML = body;
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
            .then(response => response.json())
            .then(data => {
                console.log(data);
            });
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
