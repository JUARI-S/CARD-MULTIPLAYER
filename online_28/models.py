from django.db import models
from django.conf import settings


class Room(models.Model):
    room_id = models.CharField(primary_key=True, max_length=200)
    room_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    team_a_players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_a_players')
    team_b_players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='team_b_players')
    game_started = models.BooleanField(default=False)

    # shuffling variables
    shuffler = models.CharField(default="none", max_length=200)
    seeds = models.TextField(default="[]")
    card_indices = models.TextField(default="")

    # Bidding variables
    bidder_index = models.IntegerField(default=1)
    bid_challenger_index = models.IntegerField(default=2)
    bid_value = models.IntegerField(default=16)
    bid_pass_count = models.IntegerField(default=0)
    bid_challenge_count = models.IntegerField(default=0)
    bid_last_pass = models.BooleanField(default=False)

    # Game variables
    trump = models.CharField(default="none", max_length=200)
    round_player = models.CharField(default="none", max_length=200)
    curr_player = models.CharField(default="none", max_length=200)
    team_a_points = models.IntegerField(default=0)
    team_a_target = models.IntegerField(default=0)
    team_b_points = models.IntegerField(default=0)
    team_b_target = models.IntegerField(default=0)

    def __str__(self):
        return self.room_id
    
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
    
    def get_team(self, player_name):
        return "team_a" if self.team_a_players.filter(username=player_name).exists() else "team_b"
