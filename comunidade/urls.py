from django.urls import path
from comunidade import views

urlpatterns = [
    # path (url da view, nome da função)
    path('community_create/',views.community_create,name='community_create'),
    path('my_communities/', views.my_communities, name='my_communities'),
    path('<str:nome_tag>/community_preview',views.community_preview,name='community_preview'),
    path('<str:nome_tag>/edit',views.community_edit,name="community_edit"),
    path('<str:nome_tag>/delete',views.community_delete,name="community_delete"),
    path('join/<int:community_id>/', views.join_community, name='join_community'),
    path('exit/<int:community_id>/', views.exit_community, name='exit_community'),
    path('post/<int:community_id>/',views.community_post, name="community_post"),
    path('post/<int:post_id>/delete/',views.delete_post, name="delete_post"),
    path('post/edit/',views.edit_post, name="edit_post"), # Isso não retorna um template
    path('post/like/',views.like_post, name="like_post"),
    path('post/dislike/',views.dislike_post, name="dislike_post"),
    path('musicas/',views.deezer_search,name="deezer_search"),
    path('<str:nome_tag>/community_post_page', views.community_post_page, name="community_post_page")
] 
