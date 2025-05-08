from django.shortcuts import render, redirect
from .forms import CadastroForm

def cadastro_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            # Aqui você pode salvar no banco ou só mostrar uma mensagem
            print("Usuário cadastrado:", form.cleaned_data['usuario'])
            return redirect('cadastro')  # redireciona para a mesma página ou outra
    else:
        form = CadastroForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})