from lib.Card import Card

class Player:
    """Representation of a player/agent

    Attributes:
        hand -- A tuple of the two cards in the players hand
        funds -- The funds that the player has available for betting
        current_bet -- The bet which the player has placed in the current round
    """

    def __init__(self, initial_hand: tuple[Card, Card], funds: int = 1000) -> None:
        self.hand = initial_hand
        self.funds = funds
        self.current_bet = 0
    
    def increase_bet(self, amount: int) -> None:
        """Raises the current bet by the given amount
        Precondition: The current bet must not exceed the available funds of
        the player when the amount is added to the bet.
        """
        assert (self.funds - (self.current_bet + amount) >= 0)
        self.current_bet += amount

    def __repr__(self) -> str:
        """Returns a string representation of a player"""
        c1,c2 = self.hand
        return f"({c1}, {c2})"