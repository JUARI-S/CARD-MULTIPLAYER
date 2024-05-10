from django.db import models
from django.conf import settings


class Room(models.Model):
    room_id = models.CharField(primary_key=True, max_length=200)
    room_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team_a_players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_a_players')
    team_b_players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_b_players')
    game_started = models.BooleanField(default=False)

    def __str__(self):
        return self.room_id
    
    # def players_count(self):
    #     return self.players.count()
    
    def is_room_owner(self, player):
        return player.username == self.room_owner.username
    
    def is_player_present(self, player):
        return self.team_a_players.filter(username=player.username).exists() or \
            self.team_b_players.filter(username=player.username).exists()
    
    def get_team_a_players(self):
        player_names = []
        for player in self.team_a_players.all():
            player_names.append(player.username)
        return player_names
    
    def get_team_b_players(self):
        player_names = []
        for player in self.team_b_players.all():
            player_names.append(player.username)
        return player_names
    

# class Game(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     teamA = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_a')
#     teamB = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_b')

#     def __str__(self):
#         return self.name