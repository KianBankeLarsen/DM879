import math
import tqdm
from engine import Game
from .Population import Population

def evolution(
        population_size,
        num_generations,
        round_replacement_percentage,
        percentage_of_children=0.5,
        mutation_rate=0.01,
        mutation_volatility=0.1,
        num_tournaments=5,
        tournament_rounds=1000
):
    """
    Simulates a steady state evolutionary algorithm to determine the best
    set of principle weights for a poker bot.
    """
    # Initialize population
    population = Population(population_size)
    for i in tqdm.tqdm(range(num_generations), desc="generations", leave=False):
        population.reset_bankroll()
        # Evaluation
        for individual in tqdm.tqdm(population.population, desc="individuals", leave=False):
            for _ in tqdm.tqdm(range(num_tournaments), desc="tournaments", leave=False):
                opponent = population.find_opponent(individual)
                inst = Game()
                inst.run(
                    players=[individual, opponent], tournament_rounds=tournament_rounds)
        
        if i < num_generations-1: # We do not want to change the resulting population
            # Selection, replacement and mutation
            num_replacements = max(1, math.floor(population_size*round_replacement_percentage))
            num_children = math.floor(num_replacements * percentage_of_children)
            num_dies_to_epidemic = num_replacements - num_children
            population.generate_children(num_children)
            population.epidemic(num_dies_to_epidemic)
            population.mutate_population(mutation_rate, mutation_volatility)

    return population
