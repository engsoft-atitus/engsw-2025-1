import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MusicaSalva, Playlist
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
import json

# Create your views here.

@login_required
def pesquisa_musica(request):
    user = request.user
    playlists = Playlist.objects.filter(user=request.user)  # Filtra as playlists do usuário logado (Aqui também é responsável por mostrar as playlists do usuário na lista de playlists)
    musicas_encontradas = []

    query = request.GET.get('q') 
    search_type = request.GET.get("type", "musicas")

    if search_type == "musicas" and query:
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
        print("Musicas")
        return render(request, 'buscar.html', {'musicas': musicas_encontradas, 'playlists': playlists})

    elif search_type == "playlists" and query:
        return redirect(f"{reverse('listar_playlists_todos')}?q={query}") # O reverse é responsável por redirecionar para a URL usando como ela foi definida no urls.py
    else:
        if search_type != "musicas" and search_type != "playlists":
            messages.error(request, "Por favor, selecione 'Músicas' ou 'Playlists'.")
    return render(request, 'buscar.html', {'musicas': [], 'playlists': playlists})

@login_required
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

    return render(request, 'player.html', {
        'musica': musica,
        'playlist': mark_safe(json.dumps(musicas)),
    })
    
@login_required
def salvar_musica(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        artista = request.POST.get('nomeartista')
        playlist_id = request.POST.get('playlist_id')

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user)  # Obtém a playlist do usuário logado

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

@login_required
def ver_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    
    musicas_salvas = playlist.musicas.all()  # Obtém todas as músicas salvas na playlist
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

    return render(request, 'playlist.html', {
        'musicas': musicas_encontradas,
        'playlist': playlist
    })
        
@login_required
def criar_playlist(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        user_id = request.user.id
        print(user_id)
        Playlist.objects.create(nome=nome, descricao=descricao, user_id=user_id) # Aqui não foi alterado tantas coisas, agora adiciona no banco de dados o ID do usuário logado.
        return redirect('listar_playlists')

    return render(request, 'criar_playlist.html')

@login_required
def excluir_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user) # Contém as playlists do usuário, as linhas abaixo são uma camada a mais de segurança
    if playlist.user != request.user:
        return HttpResponse("Você não tem permissão para excluir esta playlist.")
    playlist.delete()
    return redirect('listar_playlists')

@login_required
def listar_playlists_usuario(request):
    playlists = Playlist.objects.filter(user=request.user)  # Filtra pelo usuário logado
    return render(request, 'minhasPlaylists.html', {'playlists': playlists})
    

@login_required
def listar_playlists_todos(request):
    query = request.GET.get("q")
    if query:
        playlists = Playlist.objects.filter(nome__icontains=query)
    else:
        playlists = Playlist.objects.all()
    return render(request, 'playlistsTodos.html', {'playlists': playlists})