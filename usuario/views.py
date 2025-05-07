from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProfileCreationForm,UsuarioForm
from usuario.models import Usuario,Profile

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