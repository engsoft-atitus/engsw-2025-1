# Generated by Django 5.2 on 2025-06-05 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidade', '0024_community_profile_picture_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='profile_picture_hash',
            field=models.CharField(blank=True, default='afb313c562c806424d89aba46b6b64c23758e299b7fa20dfa55cb7d929317602', max_length=64, null=True),
        ),
    ]
