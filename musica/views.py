import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json


# Create your views here.
def buscar_musicas(request):
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
    return render(request, 'usuarios/buscar.html', {'musicas': musicas_encontradas})

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
    
