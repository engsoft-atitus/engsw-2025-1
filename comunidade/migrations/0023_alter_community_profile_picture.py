# Generated by Django 5.2 on 2025-06-05 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidade', '0022_alter_community_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='profile_picture',
            field=models.URLField(blank=True, default='https://tfavf9hmcaamd4yg.public.blob.vercel-storage.com/sapuca-Te78u8ZzqcKnrSdbtrhCNnMug4aV9o.jpg', null=True),
        ),
    ]
