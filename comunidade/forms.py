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
    class Meta:
        model = Post
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(),
        }