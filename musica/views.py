import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MusicaSalva, Playlist
from comunidade.models import Community
from django.contrib import messages
from django.urls import reverse
import json
from django.db.models import Q
from .forms import PlaylistForm
from django.contrib import messages
from django_project.utils import upload_vercel_image

# Create your views here.

@login_required
def pesquisa_musica(request):

    # Filtra as playlists do usuário logado (Aqui também é responsável por mostrar as playlists do usuário na lista de playlists)
    # Além disso ela também ignora playlists de curtir
    playlists = Playlist.objects.filter(user=request.user).filter(playlist_curtir = False)
    musicas_encontradas = []
    query = request.GET.get('q') 
    search_type = request.GET.get("type", "musicas")

    if search_type == "musicas" and query:
        url = f"https://api.deezer.com/search?q={query}&limit=9"
        r = requests.get(url)
        dados = r.json()
        for track in dados.get("data", []):
            musica_obj,_ = MusicaSalva.objects.get_or_create( # Pega o objeto da música
                nome=track['title'],
                artista=track['artist']['name'],
                imagem=track['album']['cover_medium'],
                defaults={'link':track['preview']} # Link não pode ser usado na query por conta
            ) # que o link pode mudar e logo iria cria uma nova música no banco

            if request.user in musica_obj.curtida.all(): # Verifica se o usuario curtiu
                curtida = True
            else:
                curtida = False

            musica = {
                'nome': musica_obj.nome,  # o nome da música
                'link': musica_obj.link,  # link de prévia da música
                'artista': musica_obj.artista,  # nome do artista
                'imagem': musica_obj.imagem,  # imagem do álbum
                'curtida': curtida # Se foi curtida ou não
            }
            
            musicas_encontradas.append(musica)

        request.session['musicas'] = musicas_encontradas    
        context = {'musicas': musicas_encontradas, 'playlists': playlists}
        
        return render(request, 'musica/buscar.html', context=context)

    elif search_type == "playlists":
        if query:
            return redirect(f"{reverse('listar_playlists_todos')}?q={query}")
        else:
            return redirect(reverse('listar_playlists_todos'))
        
    elif search_type == "usuarios" and query:
        return redirect(f"{reverse('buscar_usuario_view')}?usuario={query}")
    
    elif search_type == "comunidades" and query:
        return redirect(f"{reverse('buscar_comunidade')}?comunidade={query}")
    else:
        if search_type != "musicas" and search_type != "playlists" and search_type != "usuarios" and search_type != "comunidades":
            messages.error(request, "Por favor, selecione Músicas, Playlists ou Usuário.")

    context = {'musicas': [], 'playlists': playlists,'titulo':'Buscar'}

    return render(request, 'musica/buscar.html', context=context)

@login_required
def player(request):
    playlists = Playlist.objects.filter(user=request.user)

    nome = request.GET.get('nome')
    nomeartista = request.GET.get('nomeartista')
    linkmusica = request.GET.get('linkmusica')
    imagem = request.GET.get('imagem')

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
    
    current_index = 0
    for iteration in musicas:
        if iteration["nome"] == musica["titulo"] and iteration['artista'] == musica['artista']:
            current_index = musicas.index(iteration)
    
    return render(request, 'musica/player.html', {
        'musica': musica,
        'current_index':current_index,
        'playlist': mark_safe(json.dumps(musicas)),
        'playlists': playlists,
        'musica_obj':musica_obj,
        'playlist_curtir': playlist_curtir,
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
            messages.success(request, "Música adicionada à playlist!")
        else:
            messages.info(request, "Essa música já está na playlist.")

    return redirect('buscar_musicas')

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
                'link': track['preview'],
                'artista': track['artist']['name'],
                'imagem': track['album']['cover_medium'],
                'curtida': curtida
            }
            musicas_encontradas.append(musica_info)

        request.session['musicas'] = musicas_encontradas
    
        context = {
                   'musicas': musicas_encontradas, 
                   'playlist': playlist, 
                   'titulo': playlist.nome
                   }   

    if playlist.playlist_curtir == True:
        context.update({'playlist_curtir':True})
    return render(request, 'musica/playlist.html',context=context)

@login_required
def criar_playlist(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        user_id = request.user.id
        print(user_id)
        Playlist.objects.create(nome=nome, descricao=descricao, user_id=user_id)
        messages.success(request, "Playlist criada com sucesso!") # Aqui não foi alterado tantas coisas, agora adiciona no banco de dados o ID do usuário logado.
        return redirect('listar_playlists')

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
    return render(request, 'musica/criar_playlist.html', {'form': form})
        

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
                    return render(request, 'musica/editar_playlist.html', {'form': form, 'playlist': playlist})
            playlist.save()
            messages.success(request, "Playlist atualizada com sucesso.")
            return redirect('listar_playlists')
    else:
        form = PlaylistForm(instance=playlist)
    return render(request, 'musica/editar_playlist.html', {'form': form, 'playlist': playlist})

@login_required
def excluir_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id, user=request.user,playlist_curtir=False) # Contém as playlists do usuário, as linhas abaixo são uma camada a mais de segurança
    if playlist.user != request.user:
        return HttpResponse("Você não tem permissão para excluir esta playlist.")
    playlist.delete()
    messages.success(request, "Playlist excluída com sucesso!")
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
    return render(request, 'musica/minhasPlaylists.html', {'playlists': playlists,'titulo':'Minhas Playlists'})

@login_required
def listar_playlists_todos(request):
    query = request.GET.get("q")
    if query:
        playlists = Playlist.objects.filter(~Q(user=request.user), nome__icontains=query) # Usado o ~Q do próprio Django para filtrar, retirando as playlists que são do usuário;
    else:
        playlists = Playlist.objects.all().exclude(playlist_curtir=1)
    return render(request, 'musica/playlistsTodos.html', {'playlists': playlists})

@login_required
def buscar_usuario_view(request):
    query = request.GET.get("usuario")
    print("Query recebida:", query)
    usuarios = []
    if query:
        usuarios = User.objects.filter(username__icontains=query)[:10]
    return render(request, 'musica/busca-usuario.html', {'usuarios': usuarios })

@login_required
def buscar_comunidade(request):
    query = request.GET.get("comunidade")
    comunidades = []
    if query:
        comunidades = Community.objects.filter(nome__icontains=query)[:10]
    return render(request, 'musica/busca-comunidade.html', {'comunidades': comunidades})