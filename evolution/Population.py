from Individual import Individual
from random import random


class Population():

    def __init__(self, population_size, omega):
        """Creates a new population of n individuals"""
        self.population = [Individual() for _ in range(population_size)]
        self.omega = omega
        self.best = 0  # the highest bankroll in the population, for optimization

    def add(self, ind):
        """Adds the individual to the population"""
        self.population.append(ind)
        if self.best < ind.bankroll:
            self.best = ind.bankroll

    def remove(self, ind):
        """Removes the individual from the population"""
        self.population.remove(ind)

    def fitness(self, ind):
        """Calculates the fitness of the individual"""
        (self.omega + (self.best/ind.bankroll)**2) / (1 + 2*self.omega)

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
            tmp.append(best.copy())

        # I don't really know if we need this?
        i = 0
        while i < len(self.population):
            fit = self.fitness(self.population[i])
            if random() > fit*fit:
                self.population.pop(i)
            else:
                i = i + 1

        for i in tmp:
            self.population.append(i)
