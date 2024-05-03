from dataclasses import dataclass
from enum import Enum

from lib.Player import Player

class RoundType(Enum):
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5

@dataclass
class Round:
    """Holds the data of the meaningful values within a round of poker

    Attributes:
        is_betting_round -- Whether or not someone has raised the bet during this round
        remaining_players -- The players which have not folded in the round
        round -- Which round we are currently in (Pre-flop, Flop, Turn, River, Showdown)
        current_bet_size -- What the value of the current bet is
    """
    is_betting_round : bool
    remaining_players : list[Player]
    round : RoundType
    current_bet_size : int