# Generated by Django 5.2 on 2025-06-03 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0003_playlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='musicasalva',
            name='imagem',
            field=models.CharField(null=True),
        ),
        migrations.AddField(
            model_name='musicasalva',
            name='link',
            field=models.CharField(null=True),
        ),
    ]
