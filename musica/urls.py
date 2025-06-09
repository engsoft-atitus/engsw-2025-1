from django.urls import path
from musica import views

urlpatterns = [
    path('', views.pesquisa_musica, name='buscar_musicas'),
    path('player/', views.player, name='player'),
    path('salvar/', views.salvar_musica, name='salvar_musica'),
    path('playlists/', views.listar_playlists_usuario, name='listar_playlists'),
    path('playlists/', views.listar_playlists_todos, name='listar_playlists_todos'),
    path('playlists/todos/', views.listar_playlists_todos, name='listar_playlists_todos'),
    path('busca-usuario/', views.buscar_usuario_view, name='buscar_usuario_view'),
    path('busca-comunidade/', views.buscar_comunidade, name='buscar_comunidade'),
    path('playlist/<int:playlist_id>/', views.ver_playlist, name='ver_playlist'),
    path('playlist/<int:playlist_id>/excluir/', views.excluir_playlist, name='excluir_playlist'),
    path('criar_playlist/', views.criar_playlist, name='criar_playlist'),
    path('playlist/<int:playlist_id>/remover_musica/<int:musica_id>/', views.remover_musica_da_playlist, name='remover_musica_da_playlist'),
]