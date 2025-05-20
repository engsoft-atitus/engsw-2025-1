from django.shortcuts import render,redirect,get_object_or_404
from comunidade.forms import CommunityForm,CommunityEditForm,PostForm
from comunidade.models import Community,Community_User,Post
from django.contrib.auth.decorators import login_required

@login_required
def community_create(request):
    form = CommunityForm(request.POST,request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobre = form.cleaned_data['sobre']
            profile_picture = form.cleaned_data['profile_picture']
            
            community = Community(nome=nome,sobre=sobre,profile_picture=profile_picture,criador=request.user)
            community.nome_tag_generator()
            community.save() # Salva no banco de dados
            return redirect(my_communities) # Redireciona para outra view 
    context = {"form":form, "titulo": "Criar Comunidade"}
    return render(request,"comunidade/community_create.html",context=context)

@login_required
def community_edit(request,nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)
    if community.criador.id == request.user.id:     
        if request.method == 'POST':
            form = CommunityEditForm(request.POST,request.FILES)
            if form.is_valid():
                
                nome = form.cleaned_data['nome']
                sobre = form.cleaned_data['sobre']
                profile_picture = form.cleaned_data['profile_picture']

                community.nome = nome
                community.sobre = sobre
                if profile_picture != None:
                    community.profile_picture = profile_picture

                community.save()
                return redirect(community_preview, nome_tag=nome_tag)
        
        community = get_object_or_404(Community, nome_tag=nome_tag)
        form = CommunityEditForm(initial={'nome':community.nome,'sobre':community.sobre,
                                    'profile_picture':community.profile_picture.url})
        context = {"form":form,"community":community,"titulo": "Editar Comunidade"}
        return render(request,"comunidade/community_edit.html",context=context)
    return redirect(my_communities)

@login_required
def community_delete(request,nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)
    if community.criador.id == request.user.id:
        community.delete()
    return redirect(my_communities)

@login_required
def my_communities(request):
    user_communities = Community_User.objects.filter(user_id=request.user.id)
    community_ids = user_communities.values_list('community_id', flat=True)
    user_communities_information = Community.objects.filter(id__in=community_ids)
    
    criador_communities = Community.objects.filter(criador=request.user.id)
    criador_communities_ids = criador_communities.values_list('id',flat=True)


    communities = Community.objects.exclude(id__in=community_ids).exclude(id__in=criador_communities_ids)

    context = {"communities": communities,
               "user_communities": user_communities_information,
               "criador_communities":criador_communities,
               "titulo":"Minhas Comunidades"}
    return render(request,"comunidade/my_communities.html",context=context)

@login_required
def community_preview(request, nome_tag):
    community = get_object_or_404(Community, nome_tag=nome_tag)
    is_participating = False
    user_communities = Community_User.objects.filter(user_id=request.user.id)
    user_community_ids = user_communities.values_list('community_id', flat=True)

    posts = Post.objects.filter(community=community.id).order_by("-data_post")
    if community.id in user_community_ids:
        is_participating = True

    form = PostForm()
    context = {'community':community, 
               'is_participating': is_participating, 
               'user_id': request.user.id,
               "titulo": community.nome,
               "posts":posts,
               "form":form}

    return render(request,"comunidade/community_preview.html",context=context)

@login_required
def community_post(request,community_id):
    community = get_object_or_404(Community,id=community_id)
    form = PostForm(request.POST)
    if request.method == "POST" and form.is_valid():
        body = form.cleaned_data["body"]
        post = Post(body=body,user=request.user,community=community)
        post.save()
    return redirect(community_preview, nome_tag = community.nome_tag)

@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if not Community_User.objects.filter(user=request.user, community=community).exists() \
        and community.criador.id != request.user.id:
        community_user= Community_User.objects.create(user=request.user, community=community)
        community_user.save()

    return redirect(community_preview, nome_tag = community.nome_tag)

@login_required
def exit_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    Community_User.objects.filter(user=request.user, community=community).delete()

    return redirect(my_communities)

@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    nome_tag = post.community.nome_tag
    if post.user.id == request.user.id:
        post.delete()
    return redirect(community_preview, nome_tag = nome_tag)