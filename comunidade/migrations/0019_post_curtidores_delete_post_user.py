# Generated by Django 5.2 on 2025-05-30 23:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidade', '0018_post_curtidas_post_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='curtidores',
            field=models.ManyToManyField(related_name='curtid', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Post_User',
        ),
    ]
