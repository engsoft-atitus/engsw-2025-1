from django.shortcuts import render,redirect,get_object_or_404
from comunidade.forms import CommunityForm,CommunityEditForm
from comunidade.models import Community
from comunidade.models import Community_User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model


#todo
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
        form = CommunityEditForm(request.POST,request.FILES)
        if form.is_valid():
            community = get_object_or_404(Community, nome_tag=nome_tag)
            
            nome = form.cleaned_data['nome']
            sobre = form.cleaned_data['sobre']
            profile_picture = form.cleaned_data['profile_picture']

            community.nome = nome
            community.sobre = sobre
            if profile_picture != None:
                community.profile_picture = profile_picture

            community.save()
            return redirect(community_view, nome_tag=nome_tag)
        
    community = get_object_or_404(Community, nome_tag=nome_tag)
    form = CommunityEditForm(initial={'nome':community.nome,'sobre':community.sobre,
                                  'profile_picture':community.profile_picture.url})
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

    if request.user.is_authenticated:
        user_id = request.user.id
    
    user_communities = Community_User.objects.filter(user_id=user_id)
    community_ids = user_communities.values_list('community_id', flat=True)
    user_communities_information = Community.objects.filter(id__in=community_ids)

    print("Comunidade do usuarios: ")
    print(user_communities)
    print(user_communities_information)

    communities = Community.objects.exclude(id__in=community_ids)
    context = {"communities": communities, "user_communities": user_communities_information}
    
    return render(request,"comunidade/my_communities.html",context=context)

def community_preview(request, nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)

    is_participating = False
    if request.user.is_authenticated:
        user_id = request.user.id

        user_communities = Community_User.objects.filter(user_id=user_id)
        user_community_ids = user_communities.values_list('community_id', flat=True)

        if community.id in user_community_ids:
            is_participating = True

    context = {'community':community, 'is_participating': is_participating}
    return render(request,"comunidade/community_preview.html",context=context)

def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if not Community_User.objects.filter(user=request.user, community=community).exists():
        community_user= Community_User.objects.create(user=request.user, community=community)
        print("COmunidade-Usuario criado: ")
        print(community_user)
        community_user.save()


    return redirect('my_communities')

def exit_community(request, community_id):
    
    community = get_object_or_404(Community, id=community_id)
    Community_User.objects.filter(user=request.user, community=community).delete()
    
    print("COmunidade para ser excluida: ")
    print(community)

    return redirect(my_communities) 