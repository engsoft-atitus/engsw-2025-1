# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CadastroForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from usuario.models import Profile, Seguidor
from .forms import ProfileForm
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST

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

    is_owner = request.user == usuario
    is_private = perfil.privacidade == 0
    is_following = False

    if not is_owner:
        is_following = Seguidor.objects.filter(
            usuario=usuario,
            seguidor=request.user
        ).exists()

    context = {
        'usuario': usuario,
        'perfil': perfil,
        'is_owner': is_owner,
        'is_private': is_private,
        'is_following': is_following,
    }
    return render(request, 'usuarios/perfil.html', context)



@login_required    
def perfil_config_view(request):
    perfil, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('perfil', username=request.user.username)  # Redireciona para o perfil do usuário
    else:
        form = ProfileForm(instance=perfil)

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
    return render(request, 'usuarios/principal.html')



@login_required
def buscar_usuario_view(request):
    usuarios = []
    busca = ''
    if request.method == 'POST':
        busca = request.POST.get('usuario', '')
        usuarios = User.objects.filter(username__icontains=busca)[:10]
    return render(request, 'usuarios/buscar-usuario.html', {'usuarios': usuarios, 'busca': busca})
