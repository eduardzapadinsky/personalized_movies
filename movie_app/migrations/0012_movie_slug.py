# Generated by Django 4.0.6 on 2022-09-09 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0011_remove_movie_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
