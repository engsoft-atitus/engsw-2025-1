from django.shortcuts import render,redirect,get_object_or_404
from comunidade.forms import CommunityForm
from comunidade.models import Community
from django.contrib.auth.decorators import login_required


#todo
# - Quando editamos a comunidade, a foto é resetada, e sempre temos que colocar uma nova
# - Não postar media no git hub

@login_required
def index(request):
    communities = Community.objects.all() # Consulta todas as linhas
    context = {"communities": communities} # Context é as variáveis que vão ser usadas no template
    return render(request,"comunidade/communities.html",context=context)

def community_create(request):
    form = CommunityForm(request.POST,request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobre = form.cleaned_data['sobre']
            profile_picture = form.cleaned_data['profile_picture']
            
            community = Community(nome=nome,sobre=sobre,profile_picture=profile_picture)
            community.nome_tag_generator()
            community.save() # Salva no banco de dados
            return redirect(index) # Redireciona para outra view 
    context = {"form":form}
    return render(request,"comunidade/community_create.html",context=context)

def community_edit(request,nome_tag):    
    if request.method == 'POST':
        form = CommunityForm(request.POST,request.FILES)
        if form.is_valid():
            community = get_object_or_404(Community, nome_tag=nome_tag)
            
            nome = form.cleaned_data['nome']
            sobre = form.cleaned_data['sobre']
            profile_picture = form.cleaned_data['profile_picture']

            if nome != community.nome:
                community.nome = nome

            community.nome = nome
            community.sobre = sobre
            community.profile_picture = profile_picture

            community.save()
            return redirect(index)
    community = get_object_or_404(Community, nome_tag=nome_tag)
    form = CommunityForm(initial={'nome':community.nome,'sobre':community.sobre,
                                  'profile_picture':community.profile_picture})
    context = {"form":form,"community":community}
    return render(request,"comunidade/community_edit.html",context=context)

def community_view(request, nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)
    context = {'community':community}
    return render(request,"comunidade/community.html",context=context)

def community_delete(request,nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)
    community.delete()
    return redirect(index)

def my_communities(request):
    communities = Community.objects.all() # Consulta todas as linhas
    context = {"communities": communities} # Context é as variáveis que vão ser usadas no template
    return render(request,"comunidade/my_communities.html",context=context)

def community_preview(request, nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)
    context = {'community':community}
    return render(request,"comunidade/community_preview.html",context=context)
