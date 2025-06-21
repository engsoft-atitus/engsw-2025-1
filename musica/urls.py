from django.urls import path
from comunidade.views import community_preview
from musica import views

urlpatterns = [
    path('', views.pesquisa_musica, name='buscar_musicas'),
    path('player/', views.player, name='player'),
    path('player-comunidade/',views.player_comunidade,name='player_comunidade'),
    path('playerCurtir/', views.player, name='playerCurtir'),
    path('salvar/', views.salvar_musica, name='salvar_musica'),
    path('playlists/', views.listar_playlists_usuario, name='listar_playlists'),
    path('playlists/', views.listar_playlists_todos, name='listar_playlists_todos'),
    path('playlists/todos/', views.listar_playlists_todos, name='listar_playlists_todos'),
    path('busca-usuario/', views.buscar_usuario_view, name='buscar_usuario_view'),
    path('busca-comunidade/', views.buscar_comunidade, name='buscar_comunidade'),
    path("comunidade/<str:nome_tag>/community_preview", community_preview, name="community_preview"),
    path('playlist/<int:playlist_id>/', views.ver_playlist, name='ver_playlist'),
    path('playlist/<int:playlist_id>/excluir/', views.excluir_playlist, name='excluir_playlist'),
    path('criar_playlist/', views.criar_playlist, name='criar_playlist'),
    path('playlist/curtidas/', views.adicionarMusicasFavoritas, name='adicionarMusicasFavoritas'),
    path('playlist/descurtir/', views.excluirMusicasFavoritas, name='excluirMusicasFavoritas'),
    path('player/playlist/descurtir/', views.excluirMusicasFavoritas, name='excluirMusicasFavoritasPlayer'),
    path('player/playlist/curtidas/', views.adicionarMusicasFavoritas, name='adicionarMusicasFavoritasPlayer'),
    path('player-comunidade/playlist/descurtir/', views.excluirMusicasFavoritas, name='excluirMusicasFavoritasPlayer'),
    path('player-comunidade/playlist/curtidas/', views.adicionarMusicasFavoritas, name='adicionarMusicasFavoritasPlayer'),
    path('editar_playlist/<int:playlist_id>/editar/', views.editar_playlist, name='editar_playlist'),
    path('playlist/<int:playlist_id>/remover_musica/<int:musica_id>/', views.remover_musica_da_playlist, name='remover_musica_da_playlist'),
]