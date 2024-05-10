class UserNotInRoomException(Exception):
    """Custom exception class"""
    def __init__(self, room_id, user_name):
        self.message = f"User {user_name} is not a part of Room : {room_id}"
        super().__init__(self.message)

class GameNotStartedException(Exception):
    """Custom exception class"""
    def __init__(self, room_id):
        self.message = f"Game not started for Room : {room_id}"
        super().__init__(self.message)