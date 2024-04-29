class Card:
    """Representation of a playing card

    Attributes:
        suit -- The suit of the card (e.g. hearts or spades)
        rank -- The rank of the card (e.g. ace, 10 or jack)
        value -- The numerical value of the card (e.g. 2 is 2, jack is 11 and ace is 14)
    """

    def __init__(self, suit: str, rank: str, value: int) -> None:
        self.suit = suit
        self.rank = rank
        self.value = value

    def __repr__(self) -> str:
        return f"({self.rank}, {self.suit})"