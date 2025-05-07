from django.db import models
from django.core.validators import MinLengthValidator
from random import randint
# Create your models here.

# Classe herda da class Model
class Community(models.Model):
    nome = models.CharField(max_length=100,validators=[MinLengthValidator(5)])
    nome_tag = models.CharField(max_length=105,unique=True,validators=[MinLengthValidator(10)])
    sobre = models.CharField(max_length=256)
    profile_picture = models.ImageField(upload_to='uploads/')

    def nome_tag_generator(self):
        while True:
            id = randint(1000,9999)
            nome = f"{self.nome}_{id}"
            if not Community.objects.filter(nome_tag=nome):
                break
        self.nome_tag = nome