import enum


class Action(enum):
    """Enum of all possible actions in poker"""
    CHECK = 1 # Like saying "I'm okay with the current situation" when not in a betting round
    BET = 2 # Start a betting round by raising the bet
    CALL = 3 # Acknowledge the bet and match it
    RAISE = 4 # Raise the bet in a betting round even more
    FOLD = 5 # Drop your cards and skip the rest of the round
    ALL_IN = 6 # Maybe not nessecary?