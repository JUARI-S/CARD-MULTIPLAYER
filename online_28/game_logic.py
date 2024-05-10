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

DECK = [
    Card(CardSuit.CLUB, CardNumber.NINE),
    Card(CardSuit.CLUB, CardNumber.ACE),
    Card(CardSuit.CLUB, CardNumber.TEN),
    Card(CardSuit.CLUB, CardNumber.JACK),
    Card(CardSuit.CLUB, CardNumber.KING),
    Card(CardSuit.CLUB, CardNumber.QUEEN),
    Card(CardSuit.CLUB, CardNumber.SEVEN),
    Card(CardSuit.CLUB, CardNumber.EIGHT),
    Card(CardSuit.HEART, CardNumber.NINE),
    Card(CardSuit.HEART, CardNumber.ACE),
    Card(CardSuit.HEART, CardNumber.TEN),
    Card(CardSuit.HEART, CardNumber.JACK),
    Card(CardSuit.HEART, CardNumber.KING),
    Card(CardSuit.HEART, CardNumber.QUEEN),
    Card(CardSuit.HEART, CardNumber.SEVEN),
    Card(CardSuit.HEART, CardNumber.EIGHT),
    Card(CardSuit.DIAMOND, CardNumber.NINE),
    Card(CardSuit.DIAMOND, CardNumber.ACE),
    Card(CardSuit.DIAMOND, CardNumber.TEN),
    Card(CardSuit.DIAMOND, CardNumber.JACK),
    Card(CardSuit.DIAMOND, CardNumber.KING),
    Card(CardSuit.DIAMOND, CardNumber.QUEEN),
    Card(CardSuit.DIAMOND, CardNumber.SEVEN),
    Card(CardSuit.DIAMOND, CardNumber.EIGHT),
    Card(CardSuit.SPADE, CardNumber.NINE),
    Card(CardSuit.SPADE, CardNumber.ACE),
    Card(CardSuit.SPADE, CardNumber.TEN),
    Card(CardSuit.SPADE, CardNumber.JACK),
    Card(CardSuit.SPADE, CardNumber.KING),
    Card(CardSuit.SPADE, CardNumber.QUEEN),
    Card(CardSuit.SPADE, CardNumber.SEVEN),
    Card(CardSuit.SPADE, CardNumber.EIGHT)
]