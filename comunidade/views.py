from django.shortcuts import render,redirect,get_object_or_404
from comunidade.forms import CommunityForm,CommunityEditForm,PostForm
from comunidade.models import Community,Community_User,Post
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json 
import vercel_blob
import requests
from decouple import config

@login_required
def community_create(request):
    form = CommunityForm(request.POST,request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            nome = form.cleaned_data['nome']
            sobre = form.cleaned_data['sobre']

            profile_picture = request.FILES['profile_picture']

            # Prepare o upload para o Vercel Blob
            upload_url = 'https://blob.vercel-storage.com/upload'
            headers = {
                'Authorization': f'Bearer {config("VERCEL_BLOB_TOKEN")}'
            }
            files = {
                'file': (profile_picture.name, profile_picture.read(), profile_picture.content_type),
            }

            response = requests.post(upload_url, headers=headers, files=files)
            print(response)
            if response.status_code == 200:
                blob_data = response.json()
                blob_url = blob_data.get('url')
            else:
                blob_url = None
            community = Community(nome=nome,sobre=sobre,profile_picture=blob_url,criador=request.user)
            community.nome_tag_generator()
            community.save() # Salva no banco de dados
            return redirect(my_communities) # Redireciona para outra view 
    context = {"form":form, "titulo": "Criar Comunidade"}
    return render(request,"comunidade/community_create.html",context=context)

@login_required # Edita a comunidade
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
                #Caso enviem uma foto de perfil
                if profile_picture != None:
                    community.profile_picture = profile_picture

                community.save()
                return redirect(community_preview, nome_tag=nome_tag)
        
        community = get_object_or_404(Community, nome_tag=nome_tag)
        #Initial se refere aos valores padrões do formulário, nesse caso o valor normal da comunidade
        form = CommunityEditForm(initial={'nome':community.nome,'sobre':community.sobre,
                                    'profile_picture':community.profile_picture.url})
        context = {"form":form,"community":community,"titulo": "Editar Comunidade"}
        return render(request,"comunidade/community_edit.html",context=context)
    return redirect(my_communities)

@login_required #Deleta a comunidade
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
        post = Post.objects.create(
            body=body,
            user=request.user,
            community=community)
        post.curtidores.add(request.user)
        post.like() # O usuário já da like no seu próprio post
        post.save()
    return redirect(community_preview, nome_tag = community.nome_tag)

#Um usuário se vincula da comunidade
@login_required
def join_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)

    if not Community_User.objects.filter(user=request.user, community=community).exists() \
        and community.criador.id != request.user.id:
        community_user= Community_User.objects.create(user=request.user, community=community)
        community_user.save()

    return redirect(community_preview, nome_tag = community.nome_tag)

# Um usuário se desvincula da comunidade
@login_required
def exit_community(request, community_id):
    community = get_object_or_404(Community, id=community_id)
    Community_User.objects.filter(user=request.user, community=community).delete()

    return redirect(my_communities)

# Deleta um post da comunidade
@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    nome_tag = post.community.nome_tag
    if post.user.id == request.user.id:
        post.delete()
    return redirect(community_preview, nome_tag = nome_tag)

@login_required
def edit_post(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        post_id = json_data.get('id')
        post = get_object_or_404(Post,id=post_id)
        if post.user.id == request.user.id:
            body = json_data.get('postBody')
            if len(body) <= 500:
                post.body = body
                post.save()
                return JsonResponse({'status':'true','postBody':body},status=200)
            else:
                return JsonResponse({'status':'false','message':'Body exceeded max length of 500','postBody':post.body},status=406)
    return redirect(my_communities)

@login_required
def like_post(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        post_id = json_data.get('id')

        try:
            post = Post.objects.filter(id=post_id).get()
            post.curtidores.add(request.user)
            post.like()
            post.save()
            return JsonResponse({'status':'true'},status=200)
        except:
            return JsonResponse({'status':'false'},status=500)
    return redirect(my_communities)

@login_required
def dislike_post(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        post_id = json_data.get('id')

        try:
            post = Post.objects.filter(id=post_id).get()
            post.curtidores.remove(request.user)
            post.dislike()
            post.save()
            return JsonResponse({'status':'true'},status=200)
        except:
            return JsonResponse({'status':'false'},status=500)
    return redirect(my_communities)
