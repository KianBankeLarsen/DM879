import math
import random
import numpy as np
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from scipy.stats import truncnorm
from utils.Handstrength import estimate_hand_strength


class Model():
    def __init__(self, bankroll: int = 0):
        self.strength_threshold_bet = random.random()
        self.strength_threshold_call = random.random()
        self.aggression = random.random()
        self.betting_mean = random.random()
        self.betting_std = random.random()
        self.deceptiveness = random.random()
        self.bankroll = bankroll
        self.betting_distribution = self.get_truncated_normal()
        self.locked_attributes = ["betting_distribution"]

    def update_betting_distribution(self):
        self.betting_distribution = self.get_truncated_normal()

    def get_truncated_normal(self):
        low = 0
        high = 1
        # Ensure the mean is within the bounds
        if not (low < self.betting_mean < high):
            raise ValueError("Mean must be between low and high")

        # Ensure std is positive
        if self.betting_std <= 0:
            raise ValueError("Standard deviation must be positive")

        # Calculate the standard normal boundaries for truncation
        a, b = (low - self.betting_mean) / \
            self.betting_std, (high - self.betting_mean) / self.betting_std
        return truncnorm(a, b, loc=self.betting_mean, scale=self.betting_mean)

    def locked_attributes_append(self, attribute):
        if attribute not in self.locked_attributes:
            self.locked_attributes.append(attribute)

    def locked_attributes_remove(self, attribute):
        if attribute in self.locked_attributes:
            self.locked_attributes.remove(attribute)

    def bet_amount(self, remaining_stack):
        """Pick a bet based on remaining stack and betting distribution"""
        # print(f"beta params : {self.get_beta_params(self.betting_mean, self.betting_std)}")
        bet_dist_sample = self.betting_distribution.rvs(1)[0]
        # print(f"bet_dist_sample: {bet_dist_sample} | mean : {self.betting_mean} | std : {self.betting_std} ")
        return remaining_stack * bet_dist_sample

    def bet(self, prob_win: float, round_state, active):
        remaining_stack = round_state.stacks[active]
        min_raise, max_raise = round_state.raise_bounds()
        amount = self.bet_amount(remaining_stack)

        # confidence in bet.
        # 0.5 + aggression means that < 0.5 aggression reduces confidence, > 0.5 increases confidence
        confidence_belief = prob_win * (0.5 + self.aggression)

        # make sure that the amount is not higher than the remaining stack, and that it is at least the continue cost
        wish_to_bet = math.floor(amount * confidence_belief)
        # print(f"Wish to bet: {wish_to_bet} | Min raise: {min_raise} | Max raise: {max_raise} | prob_win: {prob_win} | confidence_belief: {confidence_belief} | amount : {amount} | aggression: {self.aggression} | remaining_stack: {remaining_stack}")
        amount = max(min_raise, min(max_raise, wish_to_bet))
        return RaiseAction(amount)

    def call(self):
        return CallAction()

    def check(self):
        return CheckAction()

    def fold(self):
        return FoldAction()

    def bluff(self, prob_win: float, round_state, active):
        # currently acts like a bet
        return self.bet(prob_win, round_state, active)

    def choose_move(self, round_state, active, n_simulations=1000):
        wins, _, _ = estimate_hand_strength(
            round_state=round_state, active=active, n_simulations=n_simulations)
        prob_win = wins / n_simulations

        legal_actions = round_state.legal_actions()
        would_like_to_bluff = RaiseAction in legal_actions and random.random() < self.deceptiveness
        # if the probability of winning is higher than the threshold for betting, then bet
        if RaiseAction in legal_actions and prob_win > self.strength_threshold_bet:
            return self.bet(prob_win, round_state, active)

        elif CallAction in legal_actions and prob_win > self.strength_threshold_call:
            return self.call()

        elif CheckAction in legal_actions and not would_like_to_bluff:
            return self.check()

        # Bluffing
        # if deception is higher than a random number [0;1), then bluff
        # deception ONLY applies to RaiseAction, as calling ~~ loosing money if you don't have a good hand
        elif would_like_to_bluff:
            return self.bluff(prob_win, round_state, active)
        else:
            return self.fold()

    def get_action(self, round_state, active):
        return self.choose_move(round_state, active)

    def inherit_traits(self, other, chance=0.05, volatility=0.1):
        allowed_attributes = [attr_name for attr_name in vars(
            self) if attr_name not in self.locked_attributes]
        for attr_name in allowed_attributes:
            if random.random() < chance:
                s_val = getattr(self, attr_name)  # self attribute
                o_val = getattr(other, attr_name)  # other attribute
                diff = s_val - o_val
                s_val += diff * volatility

                # ensure that the value is within the bounds of the attribute
                s_val = max(0, min(1, s_val))

                setattr(self, attr_name, s_val)
                if attr_name == "betting_mean" or attr_name == "betting_std":
                    self.update_betting_distribution()

    def mutate(self, volatility):
        allowed_attributes = [attr_name for attr_name in vars(
            self) if attr_name not in self.locked_attributes]
        for attr_name in allowed_attributes:
            val = getattr(self, attr_name)

            mod = val * (1 + volatility)
            mod *= 1 if random.random() < 0.5 else -1

            val = max(0, min(1, val + mod))

            setattr(self, attr_name, val)
            if attr_name == "betting_mean" or attr_name == "betting_std":
                self.update_betting_distribution()

    def generate_child(x, y):
        child = Model()
        # attributes = [attr_name for attr_name in vars(x)]
        attributes = [attr_name for attr_name in vars(
            x) if attr_name != "betting_distribution"]
        for attr_name in attributes:
            x_val = getattr(x, attr_name)
            y_val = getattr(y, attr_name)
            c_val = (x_val + y_val) / 2
            setattr(child, attr_name, c_val)

        # update distribution after getting correct mean/std values
        child.update_betting_distribution()
        return child
