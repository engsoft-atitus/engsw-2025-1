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
    profile_picture = models.ImageField()
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

    def like(self):
        self.curtidas += 1

    def dislike(self):
        self.curtidas -= 1
