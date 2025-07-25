from django import forms
from .models import Playlist

class PlaylistForm(forms.ModelForm):
    imagem = forms.ImageField(required=False)
    class Meta:
        model = Playlist
        fields = ['nome', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }