# Generated by Django 5.0.4 on 2024-05-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_28', '0011_room_seeds'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='seed',
        ),
        migrations.AddField(
            model_name='room',
            name='card_indices',
            field=models.TextField(default='[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]'),
        ),
    ]