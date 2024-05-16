import json
from enum import Enum

class CardSuit(str, Enum):
    SPADE = "spade"
    HEART = "heart"
    CLUB = "club"
    DIAMOND = "diamond"

class CardNumber(str, Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

class CardColor(Enum):
    BLACK = "black"
    RED = "red"

class Card:
    def __init__(self, suit="", number=""):
        self.suit = suit
        self.number = number

    def to_dict(self):
        return {
            "suit": self.suit,
            "number": self.number
        }
    
    def to_json(Self):
        return json.dumps(self.__dict__)

    def __str__(self):
        return self.to_json()
    
    @classmethod
    def from_json(self, json_str):
        params = json.loads(json_str)
        return cls(**params)
    
    @classmethod
    def from_dict(self, data_dict):
        obj = cls(
            suit=CardSuit(data_dict["suit"]),
            number=CardNumber(data_dict["number"])
        )