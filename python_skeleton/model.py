from collections import namedtuple
import math
import random
# from engine import Player
import numpy as np
from .skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from .skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
# import DEFucked_engine

from .utils.montecarlo_sim_handstrength import simulate_win_rate
# FoldAction = namedtuple('FoldAction', [])
# CallAction = namedtuple('CallAction', [])
# CheckAction = namedtuple('CheckAction', [])
# # we coalesce BetAction and RaiseAction for convenience
# RaiseAction = namedtuple('RaiseAction', ['amount'])

# FoldAction = DEFucked_engine.FoldAction

class Model():
    def __init__(
            self, 
            strength_threshold_bet : float = random.random(), # 0.0 - 1.0
            strength_threshold_call : float = random.random(), # 0.0 - 1.0
            aggression : float = random.random(), # 0.0 - 1.0, where 0.0:0.5 is cautious, 0.5:1.0 is aggressive
            betting_mean : float = random.random(),
            betting_std : float = random.random(), 
            deceptiveness : float = random.random(), # 0.0 - 1.0
            fitness : float = 0.0,
            bankroll : int = 0
        ):
        self.strength_threshold_bet = strength_threshold_bet
        self.strength_threshold_call = strength_threshold_call
        self.aggression = aggression
        self.betting_mean = betting_mean
        self.betting_std = betting_std
        self.deceptiveness = deceptiveness
        self.fitness = fitness
        self.bankroll = bankroll
        self.betting_distribution = np.random.normal(loc=betting_mean, scale=betting_std)
        self.locked_attributes = ["betting_distribution"]

    def update_betting_distribution(self):
        self.betting_distribution = np.random.normal(loc=self.betting_mean, scale=self.betting_std)

    def locked_attributes_append(self, attribute):
        if attribute not in self.locked_attributes:
            self.locked_attributes.append(attribute)

    def locked_attributes_remove(self, attribute):
        if attribute in self.locked_attributes:
            self.locked_attributes.remove(attribute)

    def bet_amount(self, remaining_stack):
        """Pick a bet based on remaining stack and betting distribution"""
        return math.floor(max(0, min(remaining_stack, self.betting_distribution)))

    
    def bet(self, prob_win : float, round_state, active):
        remaining_stack = round_state.stacks[active]
        amount = self.bet_amount(remaining_stack)
        
        # confidence in bet.
        # 0.5 + aggression means that < 0.5 aggression reduces confidence, > 0.5 increases confidence
        confidence_belief = prob_win * (0.5 + self.aggression)
        
        # make sure that the amount is not higher than the remaining stack
        amount = max(remaining_stack, math.floor(amount * confidence_belief))
        
        return RaiseAction(amount)
    
    def call(self):
        return CallAction()
    
    def check(self):
        return CheckAction()
    
    def fold(self):
        return FoldAction()
    
    def bluff(self, prob_win : float, round_state, active):
        # currently acts like a bet
        return self.bet(prob_win, round_state, active)
    
    def choose_move(self, round_state, active, n_simulations=1000):
        wins, losses, draws = simulate_win_rate(round_state=round_state, active=active, n_simulations=n_simulations)
        prob_win = wins / n_simulations
        
        legal_actions = round_state.legal_actions()
        # if the probability of winning is higher than the threshold for betting, then bet
        if RaiseAction in legal_actions and prob_win > self.strength_threshold_bet:
            return self.bet(prob_win, round_state, active)
        
        elif CallAction in legal_actions and prob_win > self.strength_threshold_call:
            return self.call()
        
        elif CheckAction in legal_actions:
            return self.check()
        
        # Bluffing
        # if deception is higher than a random number [0;1), then bluff
        # deception ONLY applies to RaiseAction, as calling ~~ loosing money if you don't have a good hand
        elif (RaiseAction in legal_actions) and random.random() < self.deceptiveness:
            return self.bluff(prob_win, round_state, active)
        
        else:
            return self.fold()
    
    def get_action(self, round_state, active):
        return self.choose_move(round_state, active)
    
    def inherit_traits(self, other, chance=0.05, volatility=0.1):
        allowed_attributes = [attr_name for attr_name in vars(self) if attr_name not in self.locked_attributes]
        for attr_name in allowed_attributes:
            if random.random() < chance:
                s_val = getattr(self, attr_name) # self attribute
                o_val = getattr(other, attr_name) # other attribute
                diff = s_val - o_val
                s_val += diff * volatility
                
                # ensure that the value is within the bounds of the attribute
                s_val = max(0, min(1, s_val))
                
                setattr(self, attr_name, s_val)
    
    def mutate(self, chance, volatility):
        allowed_attributes = [attr_name for attr_name in vars(self) if attr_name not in self.locked_attributes]
        for attr_name in allowed_attributes:
            if random.random() < chance:
                val = getattr(self, attr_name)
                
                mod = val * (1 + volatility)
                mod *= 1 if random.random() < 0.5 else -1
                
                val = max(0, min(1, val + mod))
                
                setattr(self, attr_name, val)
    
    def generate_child(x, y):
        child = Model() 
        attributes = [attr_name for attr_name in vars(x)]
        for attr_name in attributes:
                x_val = getattr(x, attr_name)
                y_val = getattr(y, attr_name)
                c_val = (x_val + y_val) / 2
                setattr(child, attr_name, c_val)
        
        # update distribution after getting correct mean/std values
        child.update_betting_distribution()
