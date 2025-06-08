# musica/tests/test_integracao.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from musica.models import Playlist, MusicaSalva

class TestSalvarMusicaView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='senha123')
        # Faz login com um usuário de teste.
        self.client.login(username='ana', password='senha123')
        # Cria uma playlist no banco.
        self.playlist = Playlist.objects.create(nome='Trilha de Estudo', user=self.user)

    def test_salvar_musica_em_playlist(self):
        # Simula um envio de formulário (POST) como se o usuário estivesse adicionando uma música à playlist.
        dados = {
            'nome': 'Blinding Lights',
            'nomeartista': 'The Weeknd',
            'playlist_id': self.playlist.id
        }
        response = self.client.post(reverse('salvar_musica'), dados)
        # Verifica:
        # Se o servidor respondeu corretamente (302, redirecionamento esperado).
        # Se a música foi criada no banco.
        # Se a música foi adicionada à playlist.
        self.assertEqual(response.status_code, 302)
        musica = MusicaSalva.objects.get(nome='Blinding Lights')
        self.assertIn(self.playlist, musica.playlists.all())

# Valida:
# Se a view está funcionando corretamente.
# Se o banco está sendo atualizado como esperado.
# Se o relacionamento entre objetos funciona mesmo com dados vindos de um formulário HTML real.