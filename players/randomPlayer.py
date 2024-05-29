'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import RaiseAction
from skeleton.bot import Bot
from random import randint, choice


class RandomPlayer(Bot):
    '''
    A deviously deceptive bot. 
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
        actions = [i for i in enumerate(legal_actions)]
        chosen_index = randint(0, len(actions)-1)
        chosen_action = actions[chosen_index][1]
        if chosen_action == RaiseAction:
            min_raise, max_raise = round_state.raise_bounds()
            amount = randint(min_raise, max_raise)
            return RaiseAction(amount)

        return chosen_action()
