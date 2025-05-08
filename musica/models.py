from django.db import models

# Create your models here.

class MusicaSalva(models.Model):
    nome = models.CharField(max_length=255)
    artista = models.CharField(max_length=255)

    class Meta:
        app_label = 'musica'

    def __str__(self):
        return f"{self.nome} - {self.artista}"

