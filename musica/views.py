import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MusicaSalva, Playlist
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
import json
from .forms import PlaylistForm
from django.contrib import messages
from django_project.utils import upload_vercel_image

# Create your views here.

@login_required
def pesquisa_musica(request):
    user = request.user
    playlists = Playlist.objects.filter(user=request.user).filter(playlist_curtir = False)  # Filtra as playlists do usuário logado (Aqui também é responsável por mostrar as playlists do usuário na lista de playlists)
    musicas_encontradas = []
    musicas_obj = []
    query = request.GET.get('q') 
    search_type = request.GET.get("type", "musicas")

    if search_type == "musicas" and query:
        url = f"https://api.deezer.com/search?q={query}&limit=9"
        r = requests.get(url)
        dados = r.json()
        for track in dados.get("data", []):
            musica_obj,_ = MusicaSalva.objects.get_or_create(
                nome=track['title'],
                artista=track['artist']['name'],
                imagem=track['album']['cover_medium'],
                defaults={'link':track['preview']}
            )

            if request.user in musica_obj.curtida.all():
                curtida = True
            else:
                curtida = False

            musica = {
                'nome': track['title'],  # o nome da música
                'linkmusica': track['preview'],  # link de prévia da música
                'nomeartista': track['artist']['name'],  # nome do artista
                'imagem': track['album']['cover_medium'],  # imagem do álbum
                'curtida': curtida
            }
            
            musicas_encontradas.append(musica)
            musicas_obj.append(musica_obj)
            request.session['musicas'] = musicas_encontradas
            
        return render(request, 'buscar.html', {'musicas': musicas_encontradas, 'playlists': playlists,"musicas_obj": musicas_obj})

    elif search_type == "playlists":
        if query:
            return redirect(f"{reverse('listar_playlists_todos')}?q={query}")
        else:
            return redirect(reverse('listar_playlists_todos'))
    else:
        if search_type != "musicas" and search_type != "playlists":
            messages.error(request, "Por favor, selecione 'Músicas' ou 'Playlists'.")
    return render(request, 'buscar.html', {'musicas': [], 'playlists': playlists})

@login_required
def player(request):
    playlists = Playlist.objects.filter(user=request.user)

    nome = request.GET.get('nome')
    nomeartista = request.GET.get('nomeartista')
    linkmusica = request.GET.get('linkmusica')
    imagem = request.GET.get('imagem')

    current_index = 0

    playlist_curtir = False
    if request.GET.get('playlist_curtir') == 'True':
        playlist_curtir = True
    
    musicas = request.session.get('musicas', [])
    musica = {
        'titulo': nome,
        'artista': nomeartista,
        'link': linkmusica,
        'imagem': imagem,
    }

    musica_obj = MusicaSalva.objects.filter(nome=nome, artista=nomeartista).get()
    for iteration in musicas:
        if iteration["nome"] == musica["titulo"] and iteration['nomeartista'] == musica['artista']:
            current_index = musicas.index(iteration)
    
    return render(request, 'player.html', {
        'musica': musica,
        'playlist': mark_safe(json.dumps(musicas)),
        'playlists': playlists,
        'musica_obj':musica_obj,
        'playlist_curtir': playlist_curtir,
        'current_index_equal': current_index
    })
    
@login_required
def salvar_musica(request):
    if request.method == "POST":
        nome = request.POST.get('nome')
        artista = request.POST.get('nomeartista')
        link = request.POST.get('link')
        imagem = request.POST.get('imagem')
        playlist_id = request.POST.get('playlist_id')

        playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user,playlist_curtir=False)  # Obtém a playlist do usuário logado

        # Verifica se a música já existe
        musica, criada = MusicaSalva.objects.get_or_create(
            nome=nome,
            artista=artista,
            link=link,
            imagem=imagem  
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
            
            musica_obj,_ = MusicaSalva.objects.get_or_create(
                nome=track['title'],
                artista=track['artist']['name'],
                imagem=track['album']['cover_medium'],
                defaults={'link':track['preview']}
            )

            if request.user in musica_obj.curtida.all():
                curtida = True
            else:
                curtida = False
            
            musica_info = {
                'id': musica.id,
                'nome': track['title'],
                'linkmusica': track['preview'],
                'nomeartista': track['artist']['name'],
                'imagem': track['album']['cover_medium'],
                'curtida': curtida
            }
            musicas_encontradas.append(musica_info)

        request.session['musicas'] = musicas_encontradas
    if playlist.playlist_curtir == False:
        return render(request, 'playlist.html', {
            'musicas': musicas_encontradas,
            'playlist': playlist,
        })
    else:
        return render(request, 'playlist.html', {
            'musicas': musicas_encontradas,
            'playlist': playlist,
            'playlist_curtir': True
        })

@login_required
def criar_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.user = request.user
            
            imagem = request.FILES.get('imagem')
            if imagem:
                resultado = upload_vercel_image(imagem)
                if resultado["erro"]:
                    messages.error(request, "Erro ao enviar imagem para o Vercel Blob.")
                else:
                    playlist.imagem = resultado["url"]
                    playlist.imagem_hash = resultado["file_hash"]
            playlist.save()
            return redirect('listar_playlists')
    else:
        form = PlaylistForm()
    return render(request, 'criar_playlist.html', {'form': form})
        

@login_required
def adicionarMusicasFavoritas(request):
    # Verifica se o method da requisição é post
    if request.method == "POST":
        #Pega os dados do ajax
        json_data = json.loads(request.body)
        #Pega ou cria a playlist
        try:
            playlist_curtidas, _ = Playlist.objects.get_or_create(
                nome = 'Músicas curtidas',
                descricao = 'Suas músicas curtidas',
                #O usuário nos models recebe o modelo inteiro do User e não só o id
                user = request.user,
                playlist_curtir = 1
            )
           
            nome = json_data.get('nome')
            artista = json_data.get('artista')
            #Pega ou cria a musica
            if nome != None and artista != None:
                musicaCurtida = MusicaSalva.objects.filter(nome=nome,artista=artista).get()
                musicaCurtida.curtida.add(request.user)
                musicaCurtida.playlists.add(playlist_curtidas)
                musicaCurtida.save()
                return JsonResponse({'status':'true'},status=200)
            else:
                return JsonResponse({'status':'false','message':'Body is missing parameters'},status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'status':'false','message':'Something went wrong'},status=500)
    return redirect(pesquisa_musica)

@login_required
def excluirMusicasFavoritas(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        print(json_data)
        try:
            nome = json_data.get('nome')
            artista = json_data.get('artista')
            if nome is not None and artista is not None:
                print(nome,artista)
                musicaCurtida = get_object_or_404(MusicaSalva, nome=nome, artista=artista)
                playlist_curtidas = get_object_or_404(
                    Playlist,
                    nome='Músicas curtidas',
                    descricao='Suas músicas curtidas',
                    user=request.user,
                    playlist_curtir=1
                )
                if musicaCurtida.playlists.filter(id=playlist_curtidas.id).exists():
                    musicaCurtida.playlists.remove(playlist_curtidas)
                    musicaCurtida.curtida.remove(request.user)
                    musicaCurtida.save()
                    return JsonResponse({'status': 'true'}, status=200)
                else:
                    return JsonResponse({'status': 'false', 'message': 'Music not in playlist'}, status=400)
            else:
                return JsonResponse({'status': 'false', 'message': 'Body is missing parameters'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'false', 'message': 'Something went wrong'}, status=500)

@login_required
def editar_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user,playlist_curtir=False)
    if playlist.user != request.user:
        return HttpResponse("Você não tem permissão para editar esta playlist.")
    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES, instance=playlist)
        if form.is_valid():
            playlist = form.save(commit=False)
            
            if 'imagem' in request.FILES:
                imagem = request.FILES['imagem']
                upload_result = upload_vercel_image(imagem)

                if not upload_result["erro"]:
                    playlist.imagem = upload_result["url"]
                    playlist.imagem_hash = upload_result["file_hash"]
                else:
                    messages.error(request, "Erro no upload da imagem. Tente novamente.")
                    return render(request, 'editar_playlist.html', {'form': form, 'playlist': playlist})
            playlist.save()
            messages.success(request, "Playlist atualizada com sucesso.")
            return redirect('listar_playlists')
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'editar_playlist.html', {'form': form, 'playlist': playlist})

@login_required
def excluir_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user,playlist_curtir=False) # Contém as playlists do usuário, as linhas abaixo são uma camada a mais de segurança
    if playlist.user != request.user:
        return HttpResponse("Você não tem permissão para excluir esta playlist.")
    playlist.delete()
    return redirect('listar_playlists')

@login_required
def remover_musica_da_playlist(request, playlist_id, musica_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user,playlist_curtir=False)
    if playlist.user != request.user:
        return HttpResponse("Você não tem permissão para excluir essa música.")
    musica = get_object_or_404(MusicaSalva, id=musica_id)
    playlist.musicas.remove(musica)  # remove a música da playlist (tabela ManyToMany)
    return redirect('ver_playlist', playlist_id=playlist_id)


def listar_playlists_usuario(request):
    playlists = Playlist.objects.filter(user=request.user)  # Filtra pelo usuário logado
    return render(request, 'minhasPlaylists.html', {'playlists': playlists})

@login_required
def listar_playlists_todos(request):
    query = request.GET.get("q")
    if query:
        playlists = Playlist.objects.filter(nome__icontains=query)
    else:
        playlists = Playlist.objects.all().exclude(playlist_curtir=1)
    return render(request, 'playlistsTodos.html', {'playlists': playlists})
