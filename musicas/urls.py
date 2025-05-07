from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_musicas, name='buscar_musicas'),
    path('player/', views.player, name='player'),
    path('salvar/', views.salvar_musica, name='salvar_musica'),
    path('playlist/', views.ver_playlist, name='ver_playlist'),
]
