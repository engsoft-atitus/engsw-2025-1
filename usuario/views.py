# views.py
import requests
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CadastroForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from usuario.models import Profile, Seguidor
from .forms import ProfileForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.utils.timezone import now
from django_project.utils import upload_vercel_image
from musica.models import Playlist

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            novo_usuario = User.objects.create_user(
                username=form.cleaned_data['usuario'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['senha'],
                first_name=form.cleaned_data['primeiro_nome'],
                last_name=form.cleaned_data['sobrenome']
            )
            Profile.objects.create(user=novo_usuario)
            return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']

            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=senha)
            except User.DoesNotExist:
                user = None

            if user is not None:
                login(request, user)
                return redirect('principal')
            else:
                form.add_error(None, "Credenciais inválidas.")
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})

@login_required
def perfil_view(request, username):
    usuario = get_object_or_404(User, username=username)
    perfil = get_object_or_404(Profile, user=usuario)

    # Verifica se o usuário logado é o dono do perfil
    is_owner = request.user == usuario

    # Verifica se o perfil é privado
    is_private = perfil.privacidade == 0
    # Contagem de seguidores: Quantos estão seguindo o 'usuario'
    seguidores_count = Seguidor.objects.filter(usuario=usuario).count()
    
    # Contagem de seguidos: Quantos o 'usuario' está seguindo
    seguindo_count = Seguidor.objects.filter(seguidor=usuario).count()

    # Verifica se o usuário logado está seguindo o dono do perfil
    is_following = False
    if not is_owner:
        is_following = Seguidor.objects.filter(
            usuario=usuario,
            seguidor=request.user
        ).exists()
        
    is_followed_by_user = Seguidor.objects.filter(seguidor=usuario, usuario=request.user).exists()

    context = {
        'usuario': usuario,
        'seguidores_count': seguidores_count,
        'seguindo_count': seguindo_count,
        'perfil': perfil,
        'is_owner': is_owner,
        'is_private': is_private,
        'is_following': is_following,
        'is_followed_by_user': is_followed_by_user,
        'now': now(),  # Passa a data e hora para o template, se necessário
    }
    context['bloquear_acesso'] = context['is_private'] and (
    not context['is_following'] or not context['is_followed_by_user']
    )
    return render(request, 'usuarios/perfil.html', context)


@login_required    
def perfil_config_view(request):
    # Obtém ou cria o perfil do usuário
    perfil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=perfil)

        if form.is_valid():
            # Verifica se há uma imagem de perfil
            profile_picture = form.cleaned_data.get('profile_picture')

            if profile_picture:
                # Chama a função para fazer o upload da imagem para o Vercel
                upload_dict = upload_vercel_image(profile_picture)

                if upload_dict["erro"]:
                    form.add_error('profile_picture', 'Erro ao fazer o upload da imagem.')
                else:
                    # Atualiza o perfil com a URL e o hash da imagem
                    perfil.imagem_perfil = upload_dict["url"]
                    perfil.imagem_perfil_hash = upload_dict["file_hash"]

            # Salva as alterações no perfil
            form.save()
            return redirect('perfil', username=request.user.username)

    else:
        # Caso seja uma requisição GET, exibe o formulário com os dados atuais
        form = ProfileForm(instance=perfil)

    # Renderiza a página com o formulário de perfil
    return render(request, 'usuarios/perfil-config.html', {
        'form': form,
        'perfil': perfil,
    })





    
@login_required
@require_POST
def seguir_view(request):
    user_id = request.POST.get('user_id')
    try:
        usuario = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)

    # Verifica se já está seguindo
    seguindolink = Seguidor.objects.filter(usuario=usuario, seguidor=request.user)

    if seguindolink.exists():
        # Se já segue, remove (desseguir)
        seguindolink.delete()
        status = 'unfollowed'
    else:
        # Caso contrário, cria a relação (seguir)
        Seguidor.objects.create(usuario=usuario, seguidor=request.user)
        status = 'followed'

    return JsonResponse({'status': status})


@require_POST
def logout_view(request):
    print("Logout foi chamado!")
    logout(request)
    return redirect('login')    

@login_required
def genero_view(request):
    print("entrou na view genero")

    if request.method == 'POST':
        print("entrou no if do post")
        # Captura os dados enviados via POST
        dados = request.POST.get('selectedGenres')  # Aqui estamos capturando o valor enviado como selected_Genres
        print(f"Dados recebidos: {dados}")  # Apenas para depuração, você pode remover isso mais tarde
        if dados:
            print(dados)  # Apenas para depuração, você pode remover isso mais tarde
            Profile.objects.filter(id=request.user.id).update(generos_musicas=dados)
            # Aqui você pode adicionar a lógica para processar os dados, como salvar no banco de dados ou outra operação
            return JsonResponse({'message': 'Dados recebidos com sucesso!'})
        else:
            return JsonResponse({'error': 'Nenhum dado foi enviado.'}, status=400)
    
    return render(request, 'usuarios/genero.html')


def home(request):
    return render(request, 'usuarios/home.html')

@login_required
def principal_view(request):
    playlists_destaques = playlists_destaque()
    return render(request, 'usuarios/principal.html', {'playlists_destaque': playlists_destaques})



@login_required
def buscar_usuario_view(request):
    usuarios = []
    busca = ''
    if request.method == 'POST':
        busca = request.POST.get('usuario', '')
        usuarios = User.objects.filter(username__icontains=busca)[:10]
    return render(request, 'usuarios/buscar-usuario.html', {'usuarios': usuarios, 'busca': busca})

def playlists_destaque():
    nomes = ['Pop', 'Rock', 'Hip-Hop', 'Eletrônica', 'Blues', 'Clássica', 'Jazz', 'Reggae', 'Pagode', 'Sertanejo']
    return Playlist.objects.filter(nome__in=nomes)