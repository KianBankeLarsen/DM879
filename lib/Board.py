from lib.Action import Action
from copy import deepcopy
from lib.Card import Card
from random import shuffle
from lib.Player import Player


class Board:
    """Game board of a Texas hold'em style poker board
    This class holds all the information regard a game state.

    Attributes:
        cards -- The visible cards in the middel of the table
        deck -- The deck of playing cards used
        players -- A list containing the hands of the players in the game
        current_player_index -- The index (in players) of the next person to make an action
    """

    def __init__(self, num_players: int = 4, cards: list[Card] = None, deck: list[Card] = None) -> None:
        if not 2 <= num_players <= 10:
            raise ValueError(
                "A game must have atleast 2 players and atmost 10.")
        self.cards = cards if cards else []
        self.deck = deck if deck else self.generate_deck()
        self.players = self.create_players(num_players)
        self.current_player_index = 0

    def to_move(self) -> Player:
        """Returns the player whom is next"""
        return self.players[self.current_player_index]

    def actions(self) -> list[Action]:
        """Returns a list of legal actions in the current state"""
        # TODO
        pass

    def make_action(self, a: Action) -> None:
        """Executes the action a in the setting of the current player"""
        # TODO
        pass

    def utility(self, p: Player) -> int:
        """Returns the utility of player p's hand in combination with 3 of the current community cards
        (Higher is better)
        """
        # TODO
        pass

    def is_terminal(self) -> bool:
        """Whether the current board is a finished game"""
        return len(self.players) == 1

    def generate_deck(self) -> list[Card]:
        """Generates a shuffled deck of cards"""
        ranks = ['2', '3', '4', '5', '6', '7', '8',
                 '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        deck = []

        for suit in suits:
            for i in range(len(ranks)):
                card = Card(suit, ranks[i], i+2)
                deck.append(card)

        shuffle(deck)
        return deck

    def create_players(self, num_players: int) -> list[Player]:
        """Creates num_players hands which has been drawn randomly from the deck"""
        players = []
        for _ in range(num_players):
            c1 = self.deck.pop()
            c2 = self.deck.pop()
            p = Player((c1, c2))
            players.append(p)

        return players

    def __repr__(self) -> str:
        """Returns a string representation of the board"""
        rep = ""
        rep += "Deck ---------\n"
        for c in self.deck:
            rep += f"{c}\n"
        rep += "Cards --------\n"
        rep += f"{self.cards}\n"
        rep += "Players ------\n"
        for p in self.players:
            rep += f"{p}\n"

        return rep

    def __deepcopy__(self, memo) -> any:
        """Returns a deepcopy of the current board"""
        b = Board(self.num_players, deepcopy(self.cards), deepcopy(self.deck))
        b.current_player_index = self.current_player_index
        b.players = deepcopy(self.players)
        return b
