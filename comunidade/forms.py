from django import forms
from django.forms import ModelForm
from comunidade.models import Community,Post

class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = ('nome','sobre','profile_picture')
        widgets = {
            'sobre': forms.Textarea(),
        }

class CommunityEditForm(ModelForm):
    profile_picture = forms.ImageField(required=None)
    class Meta:
        model = Community
        fields = ('nome','sobre')
        widgets = {
            'sobre': forms.Textarea(),
        }

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('body','musica')
        widgets = {
            'body': forms.Textarea(),
        }