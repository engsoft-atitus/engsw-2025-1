from django.shortcuts import render, redirect
from .forms import ProfileCreationForm,UsuarioForm,LoginForm
from usuario.models import Usuario,Profile
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate,login,logout

def cadastro_view(request):
    user_form = UsuarioForm(request.POST or None)
    profile_form = ProfileCreationForm(request.POST or None) 
    if request.method == 'POST' and user_form.is_valid() \
        and profile_form.is_valid():
        username = user_form.cleaned_data.get("username")
        email = user_form.cleaned_data.get("email")
        password = user_form.cleaned_data.get("password1")

        nascimento = profile_form.cleaned_data.get("nascimento")

        usuario = Usuario(username=username,email=email)
        usuario.set_password(password)
        usuario.save()

        profile = Profile.objects.filter(user_id=usuario.id).get()
        profile.nascimento = nascimento
        profile.save()
        return redirect(login_view)

    context = {"user_form":user_form,"profile_form":profile_form}
    return render(request,'usuarios/cadastro.html',context=context)

    """if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # Aqui você pode salvar no banco ou só mostrar uma mensagem
            print("Usuário cadastrado:", form.cleaned_data['usuario'])
            return redirect('cadastro')  # redireciona para a mesma página ou outra
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})"""

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request,email=email,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','xina'))
        
    context = {'form':form}
    return render(request,'usuarios/login.html',context=context)

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(login_view)

def xina(request):
    return render(request,'usuarios/xina.html')