from django.shortcuts import render, redirect
import requests
from .models import MusicaSalva
# Create your views here.

def buscar_musicas(request):
    musicas_encontradas = []
    query = request.GET.get('q')  # Pega o que foi digitado
    if query:
        url = f"https://api.deezer.com/search?q={query}&limit=10"
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

    return render(request, 'buscar.html', {'musicas': musicas_encontradas})

def player(request):

    nome = request.GET.get('nome')
    nomeartista = request.GET.get('nomeartista')
    linkmusica = request.GET.get('linkmusica')
    imagem = request.GET.get('imagem')

    musica = {
        'titulo': nome,
        'artista': nomeartista,
        'link': linkmusica,
        'imagem': imagem,
    }
    return render(request, 'player.html', {'musica': musica} )

def salvar_musica(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        artista = request.POST.get('nomeartista')

        print(nome)
        print(artista)

        # Evita duplicadas
        if not MusicaSalva.objects.filter(nome=nome, artista=artista).exists():
            MusicaSalva.objects.create(nome=nome, artista=artista)
            print('Música Adicionada')

    return redirect('buscar_musicas')

def ver_playlist(request):
    musicas_salvas = MusicaSalva.objects.all()
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

    return render(request, 'playlist.html', {'musicas': musicas_encontradas})