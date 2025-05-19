import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from .models import MusicaSalva, Playlist
import json


# Create your views here.
def buscar_musicas(request):
    playlists = Playlist.objects.all()
    musicas_encontradas = []
    query = request.GET.get('q')  # Pega o que foi digitado
    if query:
        url = f"https://api.deezer.com/search?q={query}&limit=9"
        r = requests.get(url)
        dados = r.json()

        for track in dados.get("data", []):
            musica = {
                'nome': track['title'],  # o nome da música
                'linkmusica': track['preview'],  # link de prévia da música
                'nomeartista': track['artist']['name'],  # nome do artista
                'imagem': track['album']['cover_medium'],  # imagem do álbum
            }
            musicas_encontradas.append(musica)
    request.session['musicas'] = musicas_encontradas
    return render(request, 'usuarios/buscar.html', {'musicas': musicas_encontradas, 'playlists': playlists})

def player(request):
    nome = request.GET.get('nome')
    nomeartista = request.GET.get('nomeartista')
    linkmusica = request.GET.get('linkmusica')
    imagem = request.GET.get('imagem')

    musicas = request.session.get('musicas', [])
    musica = {
        'titulo': nome,
        'artista': nomeartista,
        'link': linkmusica,
        'imagem': imagem,
    }
    print("JSON da playlist:", json.dumps(musicas))

    return render(request, 'player/player.html', {
        'musica': musica,
        'playlist': mark_safe(json.dumps(musicas)),
    })

def salvar_musica(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        artista = request.POST.get('nomeartista')
        playlist_id = request.POST.get('playlist_id')

        playlist = get_object_or_404(Playlist, id=playlist_id)

        # Verifica se a música já existe
        musica, criada = MusicaSalva.objects.get_or_create(
            nome=nome,
            artista=artista
        )

        # Adiciona à playlist, se ainda não estiver
        if not musica.playlists.filter(id=playlist.id).exists():
            musica.playlists.add(playlist)
            print("Música adicionada à playlist.")
        else:
            print("Música já está nessa playlist.")

    return redirect('listar_playlists')

def ver_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    musicas_salvas = playlist.musicas.all()

    musicas_encontradas = []

    for musica in musicas_salvas:
        url = f"https://api.deezer.com/search?q={musica.nome} {musica.artista}&limit=1"
        r = requests.get(url)
        dados = r.json()
        if dados.get("data"):
            track = dados["data"][0]
            musica_info = {
                'nome': track['title'],
                'linkmusica': track['preview'],
                'nomeartista': track['artist']['name'],
                'imagem': track['album']['cover_medium'],
            }
            musicas_encontradas.append(musica_info)
            print("JSON da música:", json.dumps(musica_info, indent=4))

    request.session['musicas'] = musicas_encontradas

    return render(request, 'usuarios/playlist.html', {
        'musicas': musicas_encontradas,
        'playlist': playlist
    })

def criar_playlist(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        Playlist.objects.create(nome=nome, descricao=descricao)
        return redirect('listar_playlists')

    return render(request, 'usuarios/criar_playlist.html')

def listar_playlists(request):
    playlists = Playlist.objects.all()  # ou filtrar por usuário se tiver isso depois
    return render(request, 'usuarios/minhasPlaylists.html', {'playlists': playlists})

def proxima_musica(playlist, musica_atual_nome):
    musicas = list(playlist.musicas.all())
    if not musicas:
        return None
    nomes = [m.nome for m in musicas]
    try:
        idx = nomes.index(musica_atual_nome)
    except ValueError:
        return musicas[0]
    proximo_idx = (idx + 1) % len(musicas)
    return musicas[proximo_idx]

# Exemplo de uso em uma view:
def tocar_proxima(request, playlist_id, musica_atual_nome):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    proxima = proxima_musica(playlist, musica_atual_nome)
    if not proxima:
        return redirect('ver_playlist', playlist_id=playlist_id)
    # Buscar info da Deezer
    url = f"https://api.deezer.com/search?q={proxima.nome} {proxima.artista}&limit=1"
    r = requests.get(url)
    dados = r.json()
    if dados.get("data"):
        track = dados["data"][0]
        musica_info = {
            'nome': track['title'],
            'linkmusica': track['preview'],
            'nomeartista': track['artist']['name'],
            'imagem': track['album']['cover_medium'],
        }
        return render(request, 'player/player.html', {
            'musica': musica_info,
            'playlist': mark_safe(json.dumps([musica_info])),
        })
    return redirect('ver_playlist', playlist_id=playlist_id)


