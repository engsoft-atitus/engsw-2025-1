# Generated by Django 5.2 on 2025-06-10 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musica', '0006_merge_20250610_1023'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='imagem',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='playlist',
            name='imagem_hash',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
