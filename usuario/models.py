from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(AbstractUser):
    email = models.EmailField(max_length=200,unique=True)
    username = models.CharField(max_length=100,unique=True,validators=[MinLengthValidator(5)])
    password = models.CharField(validators=[MinLengthValidator(5)])

    #usa o email como autenticador ao invés de usuário
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Profile(models.Model):
    user = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nascimento = models.DateField(null=True)

@receiver(post_save,sender=Usuario)
def update_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
