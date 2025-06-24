const searchTypeInput = document.getElementById("tipo-pesquisa");
const playlistButton = document.querySelector(".option-button:nth-child(1)");
const musicButton = document.querySelector(".option-button:nth-child(2)");
const usuariosButton = document.querySelector(".option-button:nth-child(3)");
const comunidadesButton = document.querySelector(".option-button:nth-child(4)");

searchTypeInput.value = "musicas";

searchTypeInput.value = "playlists";

searchTypeInput.value = "usuarios";

searchTypeInput.value = "comunidades";

searchTypeInput.value = "musicas";
musicButton.style.border = "5px solid #6545F0";
playlistButton.style.border = "none";
usuariosButton.style.border = "none";
comunidadesButton.style.border = "none";

musicButton.addEventListener("click", function () {
    searchTypeInput.value = "musicas";
    musicButton.style.border = "5px solid #6545F0";
    playlistButton.style.border = "none";
    usuariosButton.style.border = "none";
    comunidadesButton.style.border = "none";
});

playlistButton.addEventListener("click", function () {
    searchTypeInput.value = "playlists";
    playlistButton.style.border = "5px solid #6545F0";
    musicButton.style.border = "none";
    usuariosButton.style.border = "none";   
    comunidadesButton.style.border = "none";
});

usuariosButton.addEventListener("click", function () {
    searchTypeInput.value = "usuarios";
    usuariosButton.style.border = "5px solid #6545F0";
    musicButton.style.border = "none";
    playlistButton.style.border = "none";
    comunidadesButton.style.border = "none";
});

comunidadesButton.addEventListener("click", function () {
    searchTypeInput.value = "comunidades";
    comunidadesButton.style.border = "5px solid #6545F0";
    musicButton.style.border = "none";
    playlistButton.style.border = "none";
    usuariosButton.style.border = "none";
});