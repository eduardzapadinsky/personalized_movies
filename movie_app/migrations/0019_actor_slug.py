# Generated by Django 4.0.6 on 2022-09-12 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0018_movie_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
