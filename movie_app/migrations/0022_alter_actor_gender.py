# Generated by Django 4.0.6 on 2022-09-12 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0021_alter_actor_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='gender',
            field=models.CharField(choices=[('Чоловік', 'Чоловік'), ('Жінка', 'Жінка')], default='Чоловік', max_length=10),
        ),
    ]