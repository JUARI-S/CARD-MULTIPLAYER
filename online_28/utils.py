import random
import json

from django.contrib.auth.models import User

from online_28.config import DECK
from online_28.models import Room
from online_28.exceptions import UserNotInRoomException


def generate_room_id():
    return str(random.randint(100000, 999999))

def fetch_user(user_name):
    return User.objects.get(username=user_name)

def fetch_room(room_id, user):
    # Fetch room from roomid
    room = Room.objects.get(room_id=room_id)

    # check current user is the part of this room
    if room.is_player_present(user):
        if room.is_room_owner(user):
            return room, True
        return room, False
    else:
        raise UserNotInRoomException(room.room_id. user.username)
    
def get_cards(room):
    card_indices = json.loads(room.card_indices)
    return {
        room.get_team_a_players()[0]: [DECK[index] for index in card_indices[:8]],
        room.get_team_a_players()[1]: [DECK[index] for index in card_indices[8:16]],
        room.get_team_b_players()[0]: [DECK[index] for index in card_indices[16:24]],
        room.get_team_b_players()[1]: [DECK[index] for index in card_indices[24:32]],
    }