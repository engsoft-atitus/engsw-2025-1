function imagemMusica() {
    let audio = document.querySelector('audioPlayer');

    audio.src = element.getAttribute('data-preview-url');
    audio.play();
}