from django.urls import path
from musica import views

urlpatterns = [
    path('', views.buscar_musicas, name='buscar_musicas'),
    path('player/', views.player, name='player'),
    path('salvar/', views.salvar_musica, name='salvar_musica'),
    path('playlists/', views.listar_playlists, name='listar_playlists'),
    path('playlist/<int:playlist_id>/', views.ver_playlist, name='ver_playlist'),
    path('playlist/curtidas/', views.criar_playlist_curtidas, name='criar_playlist_curtidas'),
    path('playlist/<int:playlist_id>/excluir/', views.excluir_playlist, name='excluir_playlist'),
    path('criar_playlist/', views.criar_playlist, name='criar_playlist'),
    path('logout/', views.logout_view, name='logout'),

]