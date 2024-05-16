# Generated by Django 5.0.4 on 2024-05-15 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_28', '0018_room_bid_challenge_count_room_bid_pass_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='trump_selecter_index',
            new_name='team_a_points',
        ),
        migrations.AddField(
            model_name='room',
            name='team_a_target',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='team_b_points',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='team_b_target',
            field=models.IntegerField(default=0),
        ),
    ]
