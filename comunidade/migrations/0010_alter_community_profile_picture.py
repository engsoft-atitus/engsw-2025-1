# Generated by Django 5.2 on 2025-05-07 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comunidade', '0009_alter_community_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='profile_picture',
            field=models.ImageField(height_field=100, upload_to='uploads/', width_field=100),
        ),
    ]
