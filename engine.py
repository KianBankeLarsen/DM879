from collections import namedtuple
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
import eval7
from tqdm import tqdm

# Global attributes
STARTING_STACK = 400
BIG_BLIND = 2
SMALL_BLIND = 1
TerminalState = namedtuple('TerminalState', ['deltas', 'previous_state'])


class RoundState(namedtuple('_RoundState', ['button', 'street', 'pips', 'stacks', 'hands', 'deck', 'previous_state'])):
    '''
    Encodes the game tree for one round of poker.
    '''

    def showdown(self):
        '''
        Compares the players' hands and computes payoffs.
        '''
        score0 = eval7.evaluate(self.deck.peek(5) + self.hands[0])
        score1 = eval7.evaluate(self.deck.peek(5) + self.hands[1])
        if score0 > score1:
            delta = STARTING_STACK - self.stacks[1]
        elif score0 < score1:
            delta = self.stacks[0] - STARTING_STACK
        else:  # split the pot
            delta = (self.stacks[0] - self.stacks[1]) // 2
        return TerminalState([delta, -delta], self)

    def legal_actions(self):
        '''
        Returns a set which corresponds to the active player's legal moves.
        '''
        active = self.button % 2
        continue_cost = self.pips[1-active] - self.pips[active]
        if continue_cost == 0:
            # we can only raise the stakes if both players can afford it
            bets_forbidden = (self.stacks[0] == 0 or self.stacks[1] == 0)
            return {CheckAction} if bets_forbidden else {CheckAction, RaiseAction}
        # continue_cost > 0
        # similarly, re-raising is only allowed if both players can afford it
        raises_forbidden = (
            continue_cost == self.stacks[active] or self.stacks[1-active] == 0)
        return {FoldAction, CallAction} if raises_forbidden else {FoldAction, CallAction, RaiseAction}

    def raise_bounds(self):
        '''
        Returns a tuple of the minimum and maximum legal raises.
        '''
        active = self.button % 2
        continue_cost = self.pips[1-active] - self.pips[active]
        max_contribution = min(
            self.stacks[active], self.stacks[1-active] + continue_cost)
        min_contribution = min(
            max_contribution, continue_cost + max(continue_cost, BIG_BLIND))
        return (self.pips[active] + min_contribution, self.pips[active] + max_contribution)

    def proceed_street(self):
        '''
        Resets the players' pips and advances the game tree to the next round of betting.
        '''
        if self.street == 5:
            return self.showdown()
        new_street = 3 if self.street == 0 else self.street + 1
        return RoundState(1, new_street, [0, 0], self.stacks, self.hands, self.deck, self)

    def proceed(self, action):
        '''
        Advances the game tree by one action performed by the active player.
        '''
        active = self.button % 2
        if isinstance(action, FoldAction):
            delta = self.stacks[0] - \
                STARTING_STACK if active == 0 else STARTING_STACK - \
                self.stacks[1]
            return TerminalState([delta, -delta], self)
        if isinstance(action, CallAction):
            if self.button == 0:  # sb calls bb
                return RoundState(1, 0, [BIG_BLIND] * 2, [STARTING_STACK - BIG_BLIND] * 2, self.hands, self.deck, self)
            # both players acted
            new_pips = list(self.pips)
            new_stacks = list(self.stacks)
            contribution = new_pips[1-active] - new_pips[active]
            new_stacks[active] -= contribution
            new_pips[active] += contribution
            state = RoundState(self.button + 1, self.street,
                               new_pips, new_stacks, self.hands, self.deck, self)
            return state.proceed_street()
        if isinstance(action, CheckAction):
            if (self.street == 0 and self.button > 0) or self.button > 1:  # both players acted
                return self.proceed_street()
            # let opponent act
            return RoundState(self.button + 1, self.street, self.pips, self.stacks, self.hands, self.deck, self)
        # isinstance(action, RaiseAction)
        new_pips = list(self.pips)
        new_stacks = list(self.stacks)
        contribution = action.amount - new_pips[active]
        new_stacks[active] -= contribution
        new_pips[active] += contribution
        return RoundState(self.button + 1, self.street, new_pips, new_stacks, self.hands, self.deck, self)


class Game():
    '''
    Manages the high-level game procedure.
    '''

    def __init__(self):
        pass

    def run_round(self, players):
        '''
        Runs one round of poker.
        '''
        deck = eval7.Deck()
        deck.shuffle()
        self.hands = [deck.deal(2), deck.deal(2)]
        pips = [SMALL_BLIND, BIG_BLIND]
        stacks = [STARTING_STACK - SMALL_BLIND, STARTING_STACK - BIG_BLIND]
        round_state = RoundState(0, 0, pips, stacks, self.hands, deck, None)
        while not isinstance(round_state, TerminalState):
            active = round_state.button % 2
            player = players[active]
            action = player.get_action(round_state, active)
            round_state = round_state.proceed(action)

        for player, delta in zip(players, round_state.deltas):
            player.bankroll += delta

    def run(self, players, tournament_rounds):
        '''
        Runs one game of poker.
        '''
        p1, p2 = players[0], players[1]  # To keep track of the two players since they are swapped in the list
        for _ in tqdm(range(1, tournament_rounds + 1), desc="round", leave=False):
            self.run_round(players)
            players = players[::-1]
        return (p1.bankroll, p2.bankroll)
