from django.db import models

# Create your models here.

class Playlist(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.nome}"

class MusicaSalva(models.Model):
    nome = models.CharField(max_length=255)
    artista = models.CharField(max_length=255)
    playlists = models.ManyToManyField(Playlist, related_name='musicas')

    def __str__(self):
        return f"{self.nome} - {self.artista}"

