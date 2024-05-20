from random import random
from scipy.stats import truncnorm
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from math import floor, isclose
import numpy as np
from utils.Handstrength import estimate_hand_strength
# from engine import STARTING_STACK


class Individual():
    def __init__(self):
        """Creates a new individual.
        Each of the attributes of the individual corresponds
        to a playing principle in poker.
        """
        self.strength = random()  # Threshold of handstrength willingness
        self.aggression = random()  # Likeliness to raise
        self.deception = random()  # Induces random behaviour
        self.betting_mean = random()
        self.betting_std = random()
        self._betting_distribution = self.get_truncated_normal()
        self.bankroll = 0

    def _update_betting_distribution(self):
        self._betting_distribution = self._get_betting_distribution()

    def _get_betting_distribution(self):
        """Get the betting distribution."""
        # Calculate the standard normal boundaries for truncation
        a, b = (0 - self.betting_mean) / \
            self.betting_std, (1 - self.betting_mean) / self.betting_std
        return truncnorm(a, b, loc=self.betting_mean, scale=self.betting_mean)

    def bet_amount(self, remaining_stack):
        """Returns a bet based on remaining stack and betting distribution."""
        bet_dist_sample = self.betting_distribution.rvs(1)[0]
        return remaining_stack * bet_dist_sample

    def bet(self, prob_win: float, round_state, active):
        """Returns a raise action which raises by an amount determined
        by the betting distribution, estimated probability of
        a win (prob_win) and the remaining stack.
        """
        remaining_stack = round_state.stacks[active]
        min_raise, max_raise = round_state.raise_bounds()
        amount = self.bet_amount(remaining_stack)
        wish_to_bet = floor(amount * prob_win)
        # Bet atleast the continue cost
        amount = max(min_raise, min(max_raise, wish_to_bet))
        return RaiseAction(amount)

    def get_action(self, round_state, active):
        """Returns an action for the given round."""
        return self.choose_move(round_state, active)

    def _get_action(self, round_state, active):
        """Helper function to determine the next action."""
        # Estimate the probability of winning
        win_prop = estimate_hand_strength(
            round_state=round_state, active=active, n=1000)

        # Expected winnings
        # my_stack = round_state.stacks[active]
        # opp_stack = round_state.stacks[1-active]
        # my_contribution = STARTING_STACK - my_stack
        # opp_contribution = STARTING_STACK - opp_stack
        # continue_cost, _ = round_state.raise_bounds
        # pot_total = my_contribution + opp_contribution
        # expected_winnings = (win_prop * pot_total) - (1-win_prop) * continue_cost

        legal_actions = round_state.legal_actions()
        if RaiseAction in legal_actions:
            if win_prop + self.aggression > self.strength:
                return self.bet(win_prop, round_state, active)
            elif random() <= self.deception:  # Bluffing
                bluff_bet_prop = np.average([win_prop, self.deception])
                return self.bet(bluff_bet_prop, round_state, active)
        elif CallAction in legal_actions and isclose(win_prop, self.strength):
            return CallAction()
        elif CheckAction in legal_actions:
            return CheckAction()
        else:
            return FoldAction()

    def mutate(self, volatility):
        """"Mutates the individual"""
        allowed_attributes = [attr_name for attr_name in vars(
            self) if attr_name != "betting_distribution"]
        for attr_name in allowed_attributes:
            val = getattr(self, attr_name)
            mod = val * (1 + volatility)
            mod *= 1 if random.random() < 0.5 else -1
            val = max(0, min(1, val + mod))
            setattr(self, attr_name, val)
            if attr_name == "betting_mean" or attr_name == "betting_std":
                self._update_betting_distribution()

    def generate_child(x, y):
        """Combines the attributes of x and y by their mean"""
        child = Individual()
        attributes = [attr_name for attr_name in vars(
            x) if attr_name != "betting_distribution"]
        for attr_name in attributes:
            x_val = getattr(x, attr_name)
            y_val = getattr(y, attr_name)
            c_val = (x_val + y_val) / 2
            setattr(child, attr_name, c_val)
        # update distribution
        child._update_betting_distribution()
        return child

    def copy(self):
        """Returns a copy of the individual"""
        i = Individual()
        i.strength = self.strength
        i.aggression = self.aggression
        i.deception = self.deception
        i.betting_mean = self.betting_mean
        i.betting_std = self.betting_std
        i._update_betting_distribution()
        i.bankroll = self.bankroll
        return i