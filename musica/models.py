from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Playlist(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists', null=True)
    playlist_curtir = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome}"

class MusicaSalva(models.Model):
    nome = models.CharField(max_length=255)
    artista = models.CharField(max_length=255)
    link = models.CharField(null=True,max_length=400)
    imagem = models.CharField(null=True,max_length=300)
    playlists = models.ManyToManyField(Playlist, related_name='musicas')
    curtida = models.ManyToManyField(User,related_name='curtida')

    def __str__(self):
        return f"{self.nome} - {self.artista}"