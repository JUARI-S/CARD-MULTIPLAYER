import json
import random

from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from online_28.models import Room
from online_28.utils import fetch_room, fetch_user, get_cards
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
        self.username = self.scope["user"].username
        self.user = fetch_user(self.username)

        try:
            # Fetch room
            self.room_id = self.scope['query_string'].decode('utf-8')
            self.room, _ = fetch_room(self.room_id, self.user)

            # Fetch the team of user
            self.team = "team_a" if self.room.team_a_players.filter(username=self.user.username).exists() else "team_b"

            # players in the room
            self.queue = [self.room.get_team_a_players()[0], self.room.get_team_b_players()[0],
                          self.room.get_team_a_players()[1], self.room.get_team_b_players()[1]]
            
            # valid card suits
            self.suits = ["club", "diamond", "spade", "heart"]

            # Check is game started or not
            if not self.room.game_started:
                raise GameNotStartedException(self.room.room_id)

            # channel layer group for every player in the room
            async_to_sync(self.channel_layer.group_add)(
                self.room.room_id,
                self.channel_name
            )

            # channel layer group for this player team specific in the room
            async_to_sync(self.channel_layer.group_add)(
                f"{self.room.room_id}-{self.team}",
                self.channel_name
            )

            # channel layer group for this player specific in the room
            async_to_sync(self.channel_layer.group_add)(
                f"{self.room.room_id}-{self.user.username}",
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
        self.update_models()

        if data["type"] == "shuffler_selection":

            if self.room.shuffler == "none":
                # Rule - 3
                # Assign shuffler to a random player
                shuffler_index = random.randint(0, 3)
                shuffler = self.queue[shuffler_index]
                print("[online_28] SHUFFLER - ", shuffler)

                # Store room shuffler, bidder and bid-chalenger index
                self.room.bidder_index = (shuffler_index + 1) % 4
                self.room.bid_challenger_index = (shuffler_index + 2) % 4
                self.room.shuffler = shuffler

                # generate 3 random seeds
                seeds = []
                seeds.append(random.randint(10000, 99999))
                seeds.append(random.randint(10000, 99999))
                seeds.append(random.randint(10000, 99999))
                self.room.seeds = json.dumps(seeds)

                # Send the shuffler information to all the players
                async_to_sync(self.channel_layer.group_send)(
                    self.room.room_id,
                    {
                        'type': 'broadcast_role',
                        'data': {
                            'role': 'shuffler',
                            'value': shuffler,
                            'extras': {
                                'seed_choices': seeds
                            }
                        }
                    }
                )
            else:
                self.send(text_data = json.dumps({
                    'type': 'role_info',
                    'role_info': {
                        'role': 'shuffler',
                        'value': self.room.shuffler,
                        'extras': {
                            'seed_choices': json.loads(self.room.seeds)
                        }
                    }
                }))
        elif data["type"] == "seed_selection":
            
            # only shuffler can select the seed
            if self.user.username == self.room.shuffler:

                if data["seed_index"] <= 3 and data["seed_index"] >= 1:

                    if self.room.card_indices == "":
                        # Lock the seed 
                        seeds = json.loads(self.room.seeds)
                        seed = seeds[data["seed_index"]]
                        
                        # Set random seed and distribute the cards
                        random.seed(seed)
                        
                        # Randomly shuffle the cards among the players
                        cards_indices = [i for i in range(32)]
                        random.shuffle(cards_indices)
                        self.room.card_indices = json.dumps(cards_indices)
                        self.room.save()

                        # Assign cards on the basis of indices to every player
                        cards = get_cards(self.room)

                        # Distribute only top 4 cards among all the players
                        for player, data in cards.items():
                            async_to_sync(self.channel_layer.group_send)(
                                f"{self.room.room_id}-{player}",
                                {
                                    "type": "distribute_cards",
                                    "cards": data[:4],
                                },
                            )

                        # Broad cast the bid information
                        bidder = self.queue[self.room.bidder_index]
                        bid_challenger = self.queue[self.room.bid_challenger_index]
                        async_to_sync(self.channel_layer.group_send)(
                            self.room.room_id,
                            {
                                'type': 'broadcast_role',
                                'data': {
                                    'role': 'bid',
                                    'value': bidder,
                                    'extras': {
                                        'bidder': bidder,
                                        'bid_value': self.room.bid_value,
                                        'challenger': bid_challenger
                                    }
                                }
                            }
                        )
                    else:
                       self.send(text_data = json.dumps({
                            'type': 'error',
                            'message': 'Seed already selected'
                        })) 
                else:
                    self.send(text_data = json.dumps({
                        'type': 'error',
                        'message': 'Invalid seed index'
                    }))

            else:
                self.send(text_data = json.dumps({
                    'type': 'error',
                    'message': 'Only shuffler can select the seed'
                }))
        elif data["type"] == "bid_challenge":
            # check current user is challenger
            if self.username == self.queue[self.room.bid_challenger_index]:

                self.room.bid_challenge_count = self.room.bid_challenge_count + 1
                
                # Change the bidder and challenger
                bidder_index = self.room.bidder_index
                bid_challenger_index = self.room.bid_challenger_index
                self.room.bidder_index = bid_challenger_index
                self.room.bid_challenger_index = bidder_index

                # Update the bid value
                self.room.bid_value = self.room.bid_value + 1
                self.room.bid_last_pass = False

                # Save room
                self.room.save()

                async_to_sync(self.channel_layer.group_send)(
                    self.room.room_id,
                    {
                        'type': 'broadcast_role',
                        'data': {
                            'role': 'bid',
                            'value': self.queue[self.room.bidder_index],
                            'extras': {
                                'bidder': self.queue[self.room.bidder_index],
                                'bid_value': self.room.bid_value,
                                'challenger': self.queue[self.room.bid_challenger_index]
                            }
                        }
                    }
                )
            else:
                self.send(text_data = json.dumps({
                    'type': 'error',
                    'message': 'Only Challenger can challenge the bid'
                })) 
        elif data["type"] == "bid_pass":
            # check current user is challenger
            if self.username == self.queue[self.room.bid_challenger_index]:

                bid_pass_count = self.room.bid_pass_count + 1

                if bid_pass_count >= 3:
                    trump_selecter = self.queue[self.room.bidder_index]

                    # Set the target fopr both the teams
                    trump_Selecter_team = self.room.get_team(trump_selecter)
                    if trump_Selecter_team == "team_a":
                        self.room.team_a_target = self.room.bid_value + 1
                        self.room.team_b_target = 28 - self.room.bid_value
                    else:
                        self.room.team_a_target = 28 - self.room.bid_value
                        self.room.team_b_target = self.room.bid_value + 1

                    self.room.save()

                    # End the bidding process, start trump selection process
                    async_to_sync(self.channel_layer.group_send)(
                        self.room.room_id,
                        {
                            'type': 'broadcast_role',
                            'data': {
                                'role': 'trump_selecter',
                                'value': trump_selecter,
                                'extras': {
                                    'team_a_target': self.room.team_a_target,
                                    'team_b_target': self.room.team_b_target
                                }
                            }
                        }
                    )
                else:
                    # Change the bidder and challenger
                    bidder_index = self.room.bidder_index
                    bid_challenger_index = self.room.bid_challenger_index

                    if self.room.bid_challenge_count % 2 == 1 and not self.room.bid_last_pass:
                        bid_challenger_index = (bidder_index + 1) % 4
                    else:
                        bid_challenger_index = (bid_challenger_index + 1) % 4

                    # Save room
                    self.room.bid_challenger_index = bid_challenger_index
                    self.room.bid_pass_count = bid_pass_count
                    self.room.bid_last_pass = True
                    self.room.save()

                    async_to_sync(self.channel_layer.group_send)(
                        self.room.room_id,
                        {
                            'type': 'broadcast_role',
                            'data': {
                                'role': 'bid',
                                'value': self.queue[self.room.bidder_index],
                                'extras': {
                                    'bidder': self.queue[self.room.bidder_index],
                                    'bid_value': self.room.bid_value,
                                    'challenger': self.queue[self.room.bid_challenger_index]
                                }
                            }
                        }
                    )
            else:
                self.send(text_data = json.dumps({
                    'type': 'error',
                    'message': 'Only Challenger can pass the bid'
                })) 
        elif data["type"] == "trump_selection":
            # check current user is bidder
            if self.username == self.queue[self.room.bidder_index]:
                # check trump is already selected or not
                if self.room.trump == "none":
                    # check sanity of trump suit index
                    if data["trump_suit_index"] <= 3 and data["trump_suit_index"] >= 0:
                        # set the room trump
                        self.room.trump = self.suits[data["trump_suit_index"]]
                        self.room.round_player = self.username
                        self.room.curr_player = self.username

                        # Distribute all the cards
                        for player, data in get_cards(self.room).items():
                            async_to_sync(self.channel_layer.group_send)(
                                f"{self.room.room_id}-{player}",
                                {
                                    "type": "distribute_cards",
                                    "cards": data,
                                },
                            )

                        # Tell players about the trump (reviel only to trump selecter)
                        for player in self.queue:
                            if player == self.queue[self.room.bidder_index]:
                                async_to_sync(self.channel_layer.group_send)(
                                    f"{self.room.room_id}-{player}",
                                    {
                                        "type": "trump_info",
                                        "trump": self.room.trump,
                                    },
                                )
                            else:
                                async_to_sync(self.channel_layer.group_send)(
                                    f"{self.room.room_id}-{player}",
                                    {
                                        "type": "trump_info",
                                    },
                                )

                        # Tell player about the current player
                        async_to_sync(self.channel_layer.group_send)(
                            self.room.room_id,
                            {
                                'type': 'game_info',
                                'game_info': {
                                    'curr_player': self.username,
                                    'cards_played': []
                                }
                            }
                        )
                    else:
                        self.send(text_data = json.dumps({
                            'type': 'error',
                            'message': 'Invalid Trump index'
                        })) 
                else:
                    self.send(text_data = json.dumps({
                        'type': 'error',
                        'message': 'Trump already selected'
                    })) 
            else:
                self.send(text_data = json.dumps({
                    'type': 'error',
                    'message': 'Only Trump selecter can select the trump'
                })) 
        else:
            pass

        # store the snapshot of this room instance
        self.room.save()

    '''
    This function broadcast the role
    '''
    def broadcast_role(self, event):
        role_info = event['data']
        self.send(text_data = json.dumps({
            'type': 'role_info',
            'role_info': role_info
        }))

    '''
    This function distribute cards among players
    '''
    def distribute_cards(self, event):
        cards = event['cards']
        self.send(text_data = json.dumps({
            'type': 'cards',
            'cards': cards
        }))

    '''
    This function broadcast the trump information among players
    '''
    def trump_info(self, event):
        if event.__contains__("trump"):
            self.send(text_data = json.dumps({
                'type': 'trump_open',
                'trump': event["trump"]
            }))
        else:
            self.send(text_data = json.dumps({
                'type': 'trump_closed'
            }))

    '''
    This function broadcast game information cards played, current player
    '''
    def game_info(self, event):
        info = event['game_info']
        self.send(text_data = json.dumps({
            'type': 'game_info',
            'game_info': info
        }))

    '''
    Fetch any updates in the models
    '''
    def update_models(self):
        self.room, _ = fetch_room(self.room_id, self.user)

    '''
    This function executes when a web socket disconnected
    '''
    def disconnect(self, close_code):
        pass