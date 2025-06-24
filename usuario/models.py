from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nascimento = models.DateField(null=True, blank=True)
    generos_musicas = models.CharField(max_length=200, null=True, blank=True)
    biografia = models.TextField(null=True, blank=True)  # CLOB no Oracle, cuidado com buscas
    privacidade = models.IntegerField(default=1, choices=[(0, 'Privado'), (1, 'Público')])  # substitui BooleanField
    imagem_perfil = models.URLField(blank=True, null=True, default="https://tfavf9hmcaamd4yg.public.blob.vercel-storage.com/95e4a5e0-d81a-44d2-882b-ef0098a9235a.png")
    imagem_perfil_hash = models.CharField(max_length=64, blank=True, null=True,default="ccaae35952063bd7e441640ebfe236041947d7a9ef42576a5fc2e024a6e6be95")  # Hash da imagem para evitar duplicatas

    def __str__(self):
        return self.user.username
    
class Seguidor(models.Model):
    usuario = models.ForeignKey(User, related_name='seguidores', on_delete=models.CASCADE)
    seguidor = models.ForeignKey(User, related_name='seguidos', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('usuario', 'seguidor')  # Impede duplicatas
        verbose_name = 'Seguidor'
        verbose_name_plural = 'Seguidores'

    def __str__(self):
        return f'{self.seguidor.username} segue {self.usuario.username}'
