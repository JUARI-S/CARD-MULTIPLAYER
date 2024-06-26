# Generated by Django 5.0.4 on 2024-05-10 18:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_28', '0005_room_game_started'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='team_a_players',
            field=models.ManyToManyField(related_name='team_a_players', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='room',
            name='team_b_players',
            field=models.ManyToManyField(related_name='team_b_players', to=settings.AUTH_USER_MODEL),
        ),
    ]
