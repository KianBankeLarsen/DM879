from .Individual import Individual
from random import choice, random


class Population():

    def __init__(self, population_size):
        """Creates a new population of individuals"""
        self.population = [Individual() for _ in range(population_size)]
        
    def add(self, ind):
        """Adds the individual to the population"""
        self.population.append(ind)

    def remove(self, ind):
        """Removes the individual from the population"""
        self.population.remove(ind)

    def best(self):
        """Returns the best individual in the population"""
        best_ind = self.population[0]
        for i in self.population:
            if best_ind.bankroll < i.bankroll:
                best_ind = i
        return best_ind

    def epidemic(self, ks):
        """Simulates an epidemic on the population
        Removes the ks worst individuals from the population
        and replaces them with mutations of the best individual.
        """
        tmp = []
        best = self.best()
        for _ in range(ks):
            self._remove_worst()
            cp = best.copy()
            cp.mutate(0.1)
            tmp.append(cp)
        for i in tmp:
            self.add(i)

    def generate_children(self, children):
        self.population = sorted(self.population, key=lambda x: x.bankroll)
        for parent1_idx in range(0, children*2, 2): 
            parent2_idx = parent1_idx + 1
            child = Individual.generate_child(self.population[parent1_idx], self.population[parent2_idx])
            self._remove_worst()
            self.add(child)

    def mutate_population(self, mutation_rate, mutation_volatility):
        for individual in self.population:
            if random() < mutation_rate:
                individual.mutate(mutation_volatility)

    def reset_bankroll(self):
        """Resets the bankrolls of all individuals"""
        for i in self.population:
            i.bankroll = 0

    def find_opponent(self, ind):
        """Finds an opponent for the given individual"""
        return choice([i for i in self.population if i != ind])

    def _remove_worst(self):
        """Removes the worst individual in the population"""
        worst = self.population[0]
        i = 0
        while i < len(self.population):
            if self.population[i].bankroll < worst.bankroll:
                worst = self.population[i]
            i = i + 1

        self.population.remove(worst)
