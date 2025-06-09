const player = document.getElementById('player');
const audioSource = document.getElementById('audio-source');
const playBtn = document.getElementById("play");
const pauseBtn = document.getElementById("pause");
const progressBar = document.getElementById('progress-bar');
const progressContainer = document.querySelector('.progress-container');
const thumb = document.getElementById('progress-thumb');
let isDragging = false;

function playAudio() {
    player.play();
    playBtn.style.display = 'none';
    pauseBtn.style.display = 'inline';
}

function pauseAudio() {
    player.pause();
    pauseBtn.style.display = 'none';
    playBtn.style.display = 'inline';
}

function nextSong() {
    currentIndex = (currentIndex + 1) % playlist.length;
    const musica = playlist[currentIndex];

    audioSource.src = musica.linkmusica;
    player.load();
    player.currentTime = 0;
    player.play();

    document.querySelector('.album-img img').src = musica.imagem;
    document.querySelector('h2').innerText = musica.nome;
    document.querySelector('h3').innerText = musica.nomeartista;
}

function returnSong() {
    currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
    const musica = playlist[currentIndex];

    audioSource.src = musica.linkmusica;
    player.load();
    player.currentTime = 0;
    player.play();

    document.querySelector('.album-img img').src = musica.imagem;
    document.querySelector('h2').innerText = musica.nome;
    document.querySelector('h3').innerText = musica.nomeartista;
}

// Atualiza a barra normalmente
player.addEventListener('timeupdate', () => {
    if (!isDragging) {
        const percent = (player.currentTime / player.duration) * 100;
        progressBar.style.width = percent + '%';
        thumb.style.left = percent + '%';
    }
});

// Clique ou arraste na barra
function updateBar(e) {
    const rect = progressContainer.getBoundingClientRect();
    const offsetX = e.clientX - rect.left;
    const percent = Math.max(0, Math.min(1, offsetX / rect.width));
    const percentValue = percent * 100;

    progressBar.style.width = percentValue + '%';
    thumb.style.left = percentValue + '%';
    player.currentTime = percent * player.duration;
}

progressContainer.addEventListener('mousedown', (e) => {
    isDragging = true;
    updateBar(e);
});

document.addEventListener('mousemove', (e) => {
    if (isDragging) updateBar(e);
});

document.addEventListener('mouseup', () => {
    if (isDragging) {
        isDragging = false;
    }
});
// Atualiza o player quando a música termina
function atualizarPlayer(musica) {
    audioSource.src = musica.linkmusica;
    player.load();
    player.currentTime = 0;
    player.play();

    // Atualiza capa e texto
    document.querySelector('.album-img img').src = musica.imagem;
    document.querySelector('h2').innerText = musica.nome;
    document.querySelector('h3').innerText = musica.nomeartista;

    playBtn.style.display = 'none';
    pauseBtn.style.display = 'inline';
}
// Evento para quando a música termina
player.addEventListener('ended', () => {
    currentIndex = (currentIndex + 1) % playlist.length;
    atualizarPlayer(playlist[currentIndex]);
});