from django.test import TestCase
from usuario.models import Profile
from django.contrib.auth.models import User
from usuario.forms import ProfileForm

class ProfileFormTest(TestCase):
    def test_salvar_formulario_profile(self):
        user = User.objects.create_user(username='joao', password='123')
        perfil = Profile(user=user)

        form = ProfileForm(data={'bio': 'Nova biografia'}, instance=perfil)
        self.assertTrue(form.is_valid())

        perfil_salvo = form.save()
        self.assertEqual(perfil_salvo.bio, 'Nova biografia')
