from django.test import TestCase
from usuario.models import Profile
from django.contrib.auth.models import User
from usuario.forms import CadastroForm

class CadastroFormTest(TestCase):
    def test_cadastro_form_valido(self):
        form_data = {
            'primeiro_nome': 'Carlo',
            'sobrenome': 'Guterres',
            'usuario': 'carlo57',
            'email': 'carlo@example.com',
            'senha': 'Senha123',
            'confirmacao': 'Senha123'
        }

        form = CadastroForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
