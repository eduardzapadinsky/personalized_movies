# Generated by Django 4.0.6 on 2022-09-28 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie_app', '0044_alter_feedback_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='parent',
        ),
    ]
