# Generated by Django 4.0.6 on 2022-09-28 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0038_alter_feedback_feedback_alter_feedback_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='name',
            field=models.CharField(max_length=50, verbose_name="Ім'я"),
        ),
    ]