from django.db import models
from django.conf import settings


class Room(models.Model):
    room_id = models.CharField(max_length=200)
    room_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rooms_joined')

    def __str__(self):
        return self.name
    
    def players_count(self):
        return self.players.count()
    
    def is_player_present(self, player):
        return self.players.filter(username=player.username).exists()


class Player(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Team(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_2')

    def __str__(self):
        return self.name
    

class Game(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teamA = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a')
    teamB = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_b')

    def __str__(self):
        return self.name