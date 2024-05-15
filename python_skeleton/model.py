import math
import random
import numpy as np
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND

from utils.montecarlo_sim_handstrength import simulate_win_rate


class Model:
    def __init__(
            self, 
            strength_threshold_bet : float, # 0.0 - 1.0
            strength_threshold_call : float, # 0.0 - 1.0
            aggression : float, # 0.0 - 1.0, where 0.0:0.5 is cautious, 0.5:1.0 is aggressive
            betting_mean : float,
            betting_std : float, 
            deceptiveness : float
        ):
        self.strength_threshold_bet = strength_threshold_bet
        self.strength_threshold_call = strength_threshold_call
        self.aggression = aggression
        self.betting_mean = betting_mean
        self.betting_std = betting_std
        self.deceptiveness = deceptiveness
        self.betting_distribution = np.random.normal(loc=betting_mean, scale=betting_std)

    def bet_amount(self, remaining_stack):
        """Pick a bet based on remaining stack and betting distribution"""
        return math.floor(max(0, min(remaining_stack, self.betting_distribution())))

    
    def bet(self, prob_win : float, round_state, active):
        remaining_stack = round_state.stack[active]
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
    
    def bluff(self, prob_win : float):
        # currently acts like a bet
        return self.bet(prob_win)
    
    def choose_move(self, game_state, round_state, active, n_simulations=1000):
        wins, losses, draws = simulate_win_rate(round_state=round_state, active=active, n_simulations=n_simulations)
        prob_win = wins / n_simulations
        
        legal_actions = round_state.legal_actions()
        
        # If the probability of winning is higher than the threshold for betting, then bet
        if RaiseAction in legal_actions and prob_win > self.strength_threshold_bet:
            return self.bet(prob_win)
        
        elif CallAction in legal_actions and prob_win > self.strength_threshold_call:
            return self.call()
        
        elif CheckAction in legal_actions:
            return self.check()
        
        # Bluffing
        # If deception is higher than a random number [0;1), then bluff
        # deception ONLY applies to RaiseAction, as calling ~~ loosing money if you don't have a good hand
        elif (RaiseAction in legal_actions) and self.deceptiveness > random.random():
            return self.bluff(prob_win)
        
        else:
            return self.fold()
