from django.urls import path, include
from . import views
from musica import views

urlpatterns = [
    path('', views.buscar_musicas, name='buscar_musicas'),
    path('player/', views.player, name='player'),
    path('salvar/', views.salvar_musica, name='salvar_musica'),
    path('playlists/', views.listar_playlists, name='listar_playlists'),
    path('playlist/<int:playlist_id>/', views.ver_playlist, name='ver_playlist'),
    path('criar_playlist/', views.criar_playlist, name='criar_playlist')
]
