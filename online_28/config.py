from card_games.card import CardNumber, CardSuit, Card

# Mappings of car number with points
POINTS = {
    CardNumber.NINE: 3,
    CardNumber.ACE: 2,
    CardNumber.TEN: 2,
    CardNumber.JACK: 1,
    CardNumber.KING: 1,
    CardNumber.QUEEN: 1,
    CardNumber.SEVEN: 0,
    CardNumber.EIGHT: 0,
}

# Order of cards value
CARD_ORDER = [
    CardNumber.NINE,
    CardNumber.ACE,
    CardNumber.TEN,
    CardNumber.JACK,
    CardNumber.KING,
    CardNumber.QUEEN,
    CardNumber.SEVEN,
    CardNumber.EIGHT
]

# Deck of playing cards
DECK = [
    Card(suit=CardSuit.CLUB, number=CardNumber.NINE).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.ACE).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.TEN).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.JACK).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.KING).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.QUEEN).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.SEVEN).to_dict(),
    Card(suit=CardSuit.CLUB, number=CardNumber.EIGHT).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.NINE).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.ACE).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.TEN).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.JACK).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.KING).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.QUEEN).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.SEVEN).to_dict(),
    Card(suit=CardSuit.HEART, number=CardNumber.EIGHT).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.NINE).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.ACE).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.TEN).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.JACK).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.KING).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.QUEEN).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.SEVEN).to_dict(),
    Card(suit=CardSuit.DIAMOND, number=CardNumber.EIGHT).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.NINE).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.ACE).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.TEN).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.JACK).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.KING).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.QUEEN).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.SEVEN).to_dict(),
    Card(suit=CardSuit.SPADE, number=CardNumber.EIGHT).to_dict()
]