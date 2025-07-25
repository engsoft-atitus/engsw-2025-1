# Generated by Django 5.2 on 2025-06-09 22:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0003_playlist_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='musicasalva',
            name='curtida',
            field=models.ManyToManyField(related_name='curtida', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='playlist',
            name='playlist_curtir',
            field=models.BooleanField(default=False),
        ),
    ]
