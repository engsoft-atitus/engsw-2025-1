function toggleEdicao(element) {
if (element.querySelector(".post-body") !== null) {  
    let postBody = element.querySelector(".post-body");
    let botaoEditar = element.querySelector(".edit-post");
    let botaoDeletar = element.querySelector(".delete-post");
    
    let editPostBody = document.createElement("input");
    let botaoSalvar = document.createElement("button");
    let botaoVoltar = document.createElement("button");

    editPostBody.classList.add("post-body-edit");
    botaoSalvar.classList.add("post-save-post");
    botaoVoltar.classList.add("post-return-post"); // Return???
    botaoVoltar.setAttribute("onclick","toggleEdicao(this.parentNode)");

    postBody.replaceWith(editPostBody);
    botaoEditar.replaceWith(botaoSalvar);
    botaoDeletar.replaceWith(botaoVoltar);

    botaoSalvar.innerText = "Salvar";
    botaoVoltar.innerText = "Voltar";

} else {
    let editPostBody = element.querySelector(".post-body-edit");
    let botaoSalvar = element.querySelector(".post-save-edit");
    let botaoVoltar = element.querySelector(".post-return-post");
    
    let postBody = document.createElement("p");
    let botaoEditar = document.createElement("button");
    let botaoDeletar = document.createElement("button");

    postBody.classList.add("post-body");
    botaoEditar.classList.add("edit-post");
    botaoDeletar.classList.add("delete-post"); // Return???
    botaoEditar.setAttribute("onclick","toggleEdicao(this.parentNode)");
        
    postBody.innerText = "bola";

    console.log(botaoSalvar);

    editPostBody.replaceWith(postBody);
    botaoSalvar.replaceWith(botaoEditar);
    botaoVoltar.replaceWith(botaoDeletar);

    botaoEditar.innerText = "Editar";
    botaoDeletar.innerText = "Deletar";
}


}

function toggleButtonEdicao(){ // Cancela a edição do post,voltando ao normal
    let postBody
}