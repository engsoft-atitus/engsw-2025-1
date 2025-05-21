from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nascimento = models.DateField(null=True, blank=True)
    generos_musicas = models.CharField(max_length=200, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)
    privacidade = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
