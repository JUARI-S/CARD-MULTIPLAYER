# Generated by Django 5.0.4 on 2024-05-15 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_28', '0017_rename_bid_chalenger_index_room_bid_challenger_index'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='bid_challenge_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='bid_pass_count',
            field=models.IntegerField(default=0),
        ),
    ]
