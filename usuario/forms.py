from django import forms
import re
from django.core.exceptions import ValidationError

class CadastroForm(forms.Form):
    usuario = forms.CharField(max_length=100)
    email = forms.EmailField()
    senha = forms.CharField(widget=forms.PasswordInput)
    confirmacao = forms.CharField(widget=forms.PasswordInput)
    nascimento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if ' ' in usuario or len(usuario) < 5:
            raise ValidationError("Usuário inválido.")
        return usuario

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        regex = r'^[a-zA-Z0-9.%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, email):
            raise ValidationError("Email inválido.")
        return email

    def clean(self):
        dados = super().clean()
        senha = dados.get('senha')
        confirmacao = dados.get('confirmacao')

        if senha and (
                len(senha) < 5 or
                not re.search(r'[a-z]', senha) or
                not re.search(r'[A-Z]', senha) or
                not re.search(r'[0-9]', senha)
        ):
            raise ValidationError("A senha deve ter maiúsculas, minúsculas e números.")

        if senha != confirmacao:
            raise ValidationError("As senhas não coincidem.")
