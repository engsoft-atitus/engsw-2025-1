from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Profile

class PerfilConfigViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ana', password='senha123')
        self.client.login(username='ana', password='senha123')
        self.perfil = Profile.objects.create(user=self.user)

    def test_edicao_perfil_via_post(self):
        url = reverse('perfil_config')  # ajuste conforme o nome na URLconf
        response = self.client.post(url, {
            'bio': 'Texto atualizado',
            'privacidade': False,
        })
        self.perfil.refresh_from_db()
        self.assertRedirects(response, reverse('perfil', kwargs={'username': self.user.username}))
        self.assertEqual(self.perfil.bio, 'Texto atualizado')