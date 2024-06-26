# Generated by Django 5.0.4 on 2024-05-02 17:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('online_28', '0003_remove_player_user_remove_team_player2_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room_id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('players', models.ManyToManyField(related_name='rooms_joined', to=settings.AUTH_USER_MODEL)),
                ('room_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
