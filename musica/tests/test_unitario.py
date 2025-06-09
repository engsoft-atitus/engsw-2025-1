from django.test import TestCase
from django.contrib.auth.models import User
from musica.models import Playlist, MusicaSalva

class TestMusicaSalvaModel(TestCase):
    def setUp(self):
        # Cria um usuário de teste.
        self.user = User.objects.create_user(username='eduardo', password='senha123')
        # Cria uma playlist ligada a esse usuário.
        self.playlist = Playlist.objects.create(nome='Favoritas', user=self.user)
        # Cria uma música.
        self.musica = MusicaSalva.objects.create(nome='Shape of You', artista='Ed Sheeran')

    def test_adicionar_musica_em_playlist(self):
        # Adiciona essa música à playlist.
        self.musica.playlists.add(self.playlist)
        # Verifica se a playlist está realmente associada à música.
        self.assertIn(self.playlist, self.musica.playlists.all())

# Valida:
# Se o relacionamento ManyToMany está funcionando corretamente.
# Se o método playlists.add() está gravando no banco como esperado.





# python manage.py test --settings=test_settings
