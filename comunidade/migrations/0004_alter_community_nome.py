# Generated by Django 5.2 on 2025-04-24 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidade', '0003_community_delete_user_delete_xinamodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='nome',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
