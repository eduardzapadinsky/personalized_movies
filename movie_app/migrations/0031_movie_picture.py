# Generated by Django 4.0.6 on 2022-09-14 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0030_alter_movie_description_alter_movie_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='files/images', verbose_name='Image'),
        ),
    ]
