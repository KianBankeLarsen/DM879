'''
6.176 MIT POKERBOTS GAME ENGINE
DO NOT REMOVE, RENAME, OR EDIT THIS FILE
'''
from collections import namedtuple
from threading import Thread
from queue import Queue
import time
import json
from python_skeleton.skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from python_skeleton.model import Model
import eval7
import sys
import os

sys.path.append(os.getcwd())
from config import *
import tqdm 
# from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction

# FoldAction = namedtuple('FoldAction', [])
# CallAction = namedtuple('CallAction', [])
# CheckAction = namedtuple('CheckAction', [])
# # we coalesce BetAction and RaiseAction for convenience
# RaiseAction = namedtuple('RaiseAction', ['amount'])
TerminalState = namedtuple('TerminalState', ['deltas', 'previous_state'])

STREET_NAMES = ['Flop', 'Turn', 'River']
DECODE = {'F': FoldAction, 'C': CallAction, 'K': CheckAction, 'R': RaiseAction}
CCARDS = lambda cards: ','.join(map(str, cards))
PCARDS = lambda cards: '[{}]'.format(' '.join(map(str, cards)))
PVALUE = lambda name, value: ', {} ({})'.format(name, value)
STATUS = lambda players: ''.join([PVALUE(p.name, p.bankroll) for p in players])

# Socket encoding scheme:
#
# T#.### the player's game clock
# P# the player's index
# H**,** the player's hand in common format
# F a fold action in the round history
# C a call action in the round history
# K a check action in the round history
# R### a raise action in the round history
# B**,**,**,**,** the board cards in common format
# O**,** the opponent's hand in common format
# D### the player's bankroll delta from the round
# Q game over
#
# Clauses are separated by spaces
# Messages end with '\n'
# The engine expects a response of K at the end of the round as an ack,
# otherwise a response which encodes the player's action
# Action history is sent once, including the player's actions


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
        raises_forbidden = (continue_cost == self.stacks[active] or self.stacks[1-active] == 0)
        return {FoldAction, CallAction} if raises_forbidden else {FoldAction, CallAction, RaiseAction}

    def raise_bounds(self):
        '''
        Returns a tuple of the minimum and maximum legal raises.
        '''
        active = self.button % 2
        continue_cost = self.pips[1-active] - self.pips[active]
        max_contribution = min(self.stacks[active], self.stacks[1-active] + continue_cost)
        min_contribution = min(max_contribution, continue_cost + max(continue_cost, BIG_BLIND))
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
        # print("action : ", action)
        # print("action type : ", type(action))
        # print("FoldAction type : ", type(FoldAction()))
        # print("instance of Raise : ", isinstance(action, RaiseAction))
        # print("instance of Call : ", isinstance(action , CallAction))
        # print("instance of Check : ", isinstance(action, CheckAction))
        # print("instance of Fold : ", isinstance(action, FoldAction))
        # print("eq of Raise : ", (action == RaiseAction))
        # print("eq of Call : ", (action == CallAction))
        # print("eq of Check : ", (action== CheckAction))
        # print("eq of Fold : ", (action== FoldAction))
        # print("eq of Raise : ", (action == RaiseAction))
        # print("eq of Call : ", (action == CallAction))
        # print("eq of Check : ", (action== CheckAction))
        # print("eq of Fold : ", (action== FoldAction))
        active = self.button % 2
        if isinstance(action, FoldAction):
            delta = self.stacks[0] - STARTING_STACK if active == 0 else STARTING_STACK - self.stacks[1]
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
            state = RoundState(self.button + 1, self.street, new_pips, new_stacks, self.hands, self.deck, self)
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


class Player(Model):
    '''
    Handles subprocess and socket interactions with one player's pokerbot.
    '''

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.game_clock = STARTING_GAME_CLOCK
        self.bankroll = 0
        self.commands = None
        self.bot_subprocess = None
        self.socketfile = None
        self.bytes_queue = Queue()


    def query(self, round_state, player, active):
        '''
        Requests one action from the pokerbot over the socket connection.
        At the end of the round, we request a CheckAction from the pokerbot.
        '''
        legal_actions = round_state.legal_actions() if isinstance(round_state, RoundState) else {CheckAction}
        
        action = player.get_action(round_state, active)
        if action in legal_actions:
            if action is RaiseAction:
                amount = int(action[1:])
                min_raise, max_raise = round_state.raise_bounds()
                if min_raise <= amount <= max_raise:
                    return action(amount)
            else:
                return action()
        return CheckAction() if CheckAction in legal_actions else FoldAction()


class Game():
    '''
    Manages logging and the high-level game procedure.
    '''
    def __init__(self):
        pass

    def run_round(self, players):
        '''
        Runs one round of poker.
        '''
        deck = eval7.Deck()
        deck.shuffle()
        hands = [deck.deal(2), deck.deal(2)]
        pips = [SMALL_BLIND, BIG_BLIND]
        stacks = [STARTING_STACK - SMALL_BLIND, STARTING_STACK - BIG_BLIND]
        round_state = RoundState(0, 0, pips, stacks, hands, deck, None)
        while not isinstance(round_state, TerminalState):
            active = round_state.button % 2
            player = players[active]
            action = player.get_action(round_state, active)
            round_state = round_state.proceed(action)
        for player, delta in zip(players, round_state.deltas):
            # action = player.get_action(round_state, active)
            player.bankroll += delta

    def run(self, players, tournament_rounds):
        '''
        Runs one game of poker.
        '''
        print('   __  _____________  ___       __           __        __    ')
        print('  /  |/  /  _/_  __/ / _ \\___  / /_____ ____/ /  ___  / /____')
        print(' / /|_/ // /  / /   / ___/ _ \\/  \'_/ -_) __/ _ \\/ _ \\/ __(_-<')
        print('/_/  /_/___/ /_/   /_/   \\___/_/\\_\\\\__/_/ /_.__/\\___/\\__/___/')
        print()
        print('Starting the Pokerbots engine...')
        for _ in tqdm.tqdm(range(1, tournament_rounds + 1)):
            self.run_round(players)
            players = players[::-1]
        return [p.bankroll for p in players]
