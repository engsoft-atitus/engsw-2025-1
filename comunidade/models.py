from django.db import models
from musica.models import MusicaSalva
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

from django.core.validators import MinLengthValidator,MinValueValidator
from random import randint

# Classe herda da class Model
class Community(models.Model):
    User = get_user_model()
    nome = models.CharField(max_length=100,validators=[MinLengthValidator(5)])
    nome_tag = models.CharField(max_length=105,unique=True,validators=[MinLengthValidator(10)])
    sobre = models.CharField(max_length=256)
    profile_picture = models.URLField(blank=True,null=True,default="https://tfavf9hmcaamd4yg.public.blob.vercel-storage.com/b4864697-cf52-4e20-a2d1-ebbd3b8a3a5c.jpg")
    profile_picture_hash = models.CharField(max_length=64,null=True,blank=True,default="afb313c562c806424d89aba46b6b64c23758e299b7fa20dfa55cb7d929317602")
    criador = models.ForeignKey(User,on_delete=models.CASCADE)

    def nome_tag_generator(self):
        while True:
            id = randint(1000,9999)
            nome = f"{self.nome}_{id}"
            if not Community.objects.filter(nome_tag=nome):
                break
        self.nome_tag = nome
    def __str__(self):
        return f"{self.nome} (@{self.nome_tag})"

class Community_User(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.email} - {self.community.nome_tag}"  # ou outro campo relevante

class Post(models.Model):
    User = get_user_model()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    data_post = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community,on_delete=models.CASCADE)
    musica = models.ForeignKey(MusicaSalva,null=True,on_delete=models.CASCADE)
    curtidas = models.IntegerField(validators=[MinValueValidator(0)],default=0)

    curtidores = models.ManyToManyField(User,related_name='curtidores')

    def __str__(self):
        return f"{self.id}"