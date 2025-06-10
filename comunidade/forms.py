from django import forms
from django.forms import ModelForm
from comunidade.models import Community,Post

class CommunityForm(ModelForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = Community
        fields = ('nome','sobre',)
        widgets = {
            'sobre': forms.Textarea(),
        }

class CommunityEditForm(ModelForm):
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = Community
        fields = ('nome','sobre')
        widgets = {
            'sobre': forms.Textarea(),
        }

class PostForm(ModelForm):
    musica_nome = forms.CharField(required=None)
    musica_artista = forms.CharField(required=None)
    musica_link = forms.CharField(required=None)
    musica_imagem = forms.CharField(required=None)
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(),
        }