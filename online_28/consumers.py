import json
import random

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from online_28.models import Room
from online_28.utils import fetch_room, fetch_user
from online_28.exceptions import GameNotStartedException, UserNotInRoomException


class LobbyConsumer(WebsocketConsumer):
    
    '''
    This function executes when a new web socket connection arrives
    '''
    def connect(self):

        # Fetch user details
        self.user = fetch_user(self.scope["user"].username)

        try:
            # Fetch room
            self.room, self.owner = fetch_room(self.scope['query_string'].decode('utf-8'), self.user)

            # Fetch the team of user
            self.team = "team_a" if self.room.team_a_players.filter(username=self.user.username).exists() else "team_b"

            # Join this user channel in channel layer
            async_to_sync(self.channel_layer.group_add)(
                self.room.room_id,
                self.channel_name
            )

            # Send a message to all users in room about the members present in the lobby
            async_to_sync(self.channel_layer.group_send)(
                self.room.room_id,
                {
                    'type': 'lobby_info',
                    'team_a_players': self.room.get_team_a_players(),
                    'team_b_players': self.room.get_team_b_players()
                }
            )
            status = 'success'
            message = 'Connection successful'

        except Room.DoesNotExist:
            status = 'failed'
            message = 'Invalid Room ID'
        except UserNotInRoomException:
            status = 'failed'
            message = 'Current user is not the part of this room'

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'lobby_status',
            'status': status,
            'message': message
        }))

    '''
    This function executes when a web socket connection client sends something
    '''
    def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "change_team":
            
            if self.team == "team_a" and self.room.team_b_players.count() <= 1:
                self.room.team_a_players.remove(self.user)
                self.room.team_b_players.add(self.user)
                self.team = "team_b"

                # Update other user UI for the players infor in the room
                async_to_sync(self.channel_layer.group_send)(
                    self.room.room_id,
                    {
                        'type': 'lobby_info',
                        'team_a_players': self.room.get_team_a_players(),
                        'team_b_players': self.room.get_team_b_players()
                    }
                )
            elif self.team == "team_b" and self.room.team_a_players.count() <= 1:
                self.room.team_b_players.remove(self.user)
                self.room.team_a_players.add(self.user)
                self.team = "team_a"

                # Update other user UI for the players infor in the room
                async_to_sync(self.channel_layer.group_send)(
                    self.room.room_id,
                    {
                        'type': 'lobby_info',
                        'team_a_players': self.room.get_team_a_players(),
                        'team_b_players': self.room.get_team_b_players()
                    }
                )
            else:
                self.send(text_data = json.dumps({
                    'type': 'error',
                    'message': 'Team B is full' if self.team == "team_a" else 'Team A is full'
                }))

        elif data["type"] == "leave_room":
            
            # Remove this user from this room
            if self.team == "team_a":
                self.room.team_a_players.remove(self.user)
            else:
                self.room.team_b_players.remove(self.user)

            # Update other user UI for the players infor in the room
            async_to_sync(self.channel_layer.group_send)(
                self.room.room_id,
                {
                    'type': 'lobby_info',
                    'team_a_players': self.room.get_team_a_players(),
                    'team_b_players': self.room.get_team_b_players()
                }
            )

            # remove player channel from this channel_layer group
            async_to_sync(self.channel_layer.group_discard)(
                self.room.room_id,
                self.channel_name
            )

        elif data["type"] == "delete_room":

            # Update other user that room is going to be deleted plz leave
            async_to_sync(self.channel_layer.group_send)(
                self.room.room_id,
                {
                    'type': 'lobby_info',
                    'team_a_players': [],
                    'team_b_players': []
                }
            )

            # Delete this room
            self.room.delete()

        elif data["type"] == "start_game":
            
            # velidation on server-side
            if self.room.team_a_players.count() == 2 and self.room.team_b_players.count() == 2:
                # Start the game
                self.room.game_started = True
                self.room.save()
                
                # Update other user that room is going to be deleted plz leave
                async_to_sync(self.channel_layer.group_send)(
                    self.room.room_id,
                    {
                        'type': 'start_game'
                    }
                )
            else:
                self.send(text_data = json.dumps({
                    'type': 'error',
                    'message': 'Let the other player join the room !!'
                }))
        else:
            self.send(text_data = json.dumps({
                'type': 'error',
                'message': 'Invalid data type'
            }))

    '''
    Function to broadcast the lobby information to every user in that room
    '''
    def lobby_info(self, event):
        team_a_players = event['team_a_players']
        team_b_players = event['team_b_players']
        self.send(text_data = json.dumps({
            'type': 'lobby_info',
            'team_a_players': team_a_players,
            'team_b_players': team_b_players
        }))

    '''
    Function to broadcast the start of game
    '''
    def start_game(self, event):
        self.send(text_data = json.dumps({
            'type': 'start_game'
        }))

    '''
    This function executes when a web socket disconnected
    '''
    def disconnect(self, close_code):
        if(self.owner) :
            # delete the room
            pass
        else :
            # remove user from the room
            pass

class GameConsumer(WebsocketConsumer):
    
    '''
    This function executes when a new web socket connection arrives
    '''
    def connect(self):

        # Fetch user details
        self.user = fetch_user(self.scope["user"].username)

        try:
            # Fetch room
            self.room, _ = fetch_room(self.scope['query_string'].decode('utf-8'), self.user)

            # Fetch the team of user
            self.team = "team_a" if self.room.team_a_players.filter(username=self.user.username).exists() else "team_b"

            # Check is game started or not
            if not self.room.game_started:
                raise GameNotStartedException(self.room.room_id)

            # Join this user channel in channel layer
            async_to_sync(self.channel_layer.group_add)(
                self.room.room_id,
                self.channel_name
            )

            status = 'success'
            message = 'Connection successful'

        except Room.DoesNotExist:
            status = 'failed'
            message = 'Invalid Room ID'
        except UserNotInRoomException as e:
            status = 'failed'
            message = e.message
        except GameNotStartedException as e:
            status = 'failed'
            message = e.message

        self.accept()

        self.send(text_data=json.dumps({
            'type': 'game_status',
            'status': status,
            'message': message
        }))

    '''
    This function executes when a web socket connection client sends something
    '''
    def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "shuffler_selection":
            # Rule - 3
            # Assign shuffler to a random player
            shuffler_index = random.randint(0, 3)
            self.shuffler = self.room.get_team_a_players()[shuffler_index] if shuffler_index <= 1 else self.room.get_team_b_players()[shuffler_index-2]
            print("SHUFFLER - ", self.shuffler)

            # generate 3 random seeds
            self.seeds = [555, 333, 444]

            # Send the shuffler information to all the players
            async_to_sync(self.channel_layer.group_send)(
                self.room.room_id,
                {
                    'type': 'broadcast_role',
                    'data': {
                        'role': 'shuffler',
                        'value': self.shuffler,
                        'extras': {
                            'seed_choices': self.seeds
                        }
                    }
                }
            )
        else:
            pass

    '''
    This function broadcast the role
    '''
    def broadcast_role(self, event):
        role_info = event['data']
        self.send(text_data = json.dumps({
            'type': 'role_info',
            'data': role_info
        }))

    '''
    This function executes when a web socket disconnected
    '''
    def disconnect(self, close_code):
        pass