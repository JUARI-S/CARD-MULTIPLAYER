# Generated by Django 5.0.4 on 2024-05-10 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_28', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='game_started',
            field=models.BooleanField(default=False),
        ),
    ]
