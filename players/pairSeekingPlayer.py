'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import CallAction, RaiseAction, CheckAction
from skeleton.bot import Bot


class PairSeekingPlayer(Bot):
    '''
    A pair seeking bot which goes all in on pairs and checks otherwise.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        self.bankroll = 0

    def get_action(self, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        my_cards = round_state.hands[active]
        street = round_state.street
        board_cards = round_state.deck[:street]
        actions = [i[1] for i in enumerate(legal_actions)]
        can_check = CheckAction in actions

        ## Accessing the types of cards and discarding the suit
        c1 = str(my_cards[0])[0]
        c2 = str(my_cards[1])[0]
        cards = [c1, c2]
        for c in board_cards:
            c_type = str(c)[0]
            cards.append(c_type)
        my_stack = round_state.stacks[active]
        if len(cards) > len(set(cards)) and my_stack > 0:
            _, max_raise = round_state.raise_bounds()
            return RaiseAction(max_raise)
        elif can_check:
            return CheckAction()
        else:
            return CallAction()
