from django import forms
from django.forms import ModelForm
from comunidade.models import Community

class CommunityForm(ModelForm):
    class Meta:
        model = Community
        fields = ('nome','sobre','profile_picture')
        widgets = {
            'sobre': forms.Textarea(),
        }
