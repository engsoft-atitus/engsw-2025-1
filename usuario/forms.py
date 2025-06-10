from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re
from .models import Profile

User = get_user_model()

class CadastroForm(forms.Form):
    primeiro_nome = forms.CharField(max_length=30, label="Nome")
    sobrenome = forms.CharField(max_length=150, label="Sobrenome")
    usuario = forms.CharField(max_length=150, label="Usuário")
    email = forms.EmailField(max_length=255, required=True, label="E-mail")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    confirmacao = forms.CharField(widget=forms.PasswordInput, label="Confirmação de Senha")

    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if ' ' in usuario or len(usuario) < 5:
            raise ValidationError("Usuário inválido.")
        if User.objects.filter(username=usuario).exists():
            raise ValidationError("Este nome de usuário já está em uso.")
        return usuario

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean(self):
        dados = super().clean()
        senha = dados.get('senha')
        confirmacao = dados.get('confirmacao')

        if senha:
            if (
                len(senha) < 5 or
                not re.search(r'[a-z]', senha) or
                not re.search(r'[A-Z]', senha) or
                not re.search(r'[0-9]', senha)
            ):
                self.add_error('senha', "A senha deve ter maiúsculas, minúsculas e números.")
        
        if senha != confirmacao:
            self.add_error('confirmacao', "As senhas não coincidem.")
        return dados




class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    
class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['nascimento', 'biografia', 'privacidade']
        widgets = {
            'nascimento': forms.DateInput(attrs={'type': 'date'}),
            'biografia': forms.Textarea(attrs={'rows': 4}),
        }

