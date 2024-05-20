import math
import random
import tqdm
from engine import Game
from model import Model


def evolutionary_algorithm(
        population_size,
        num_generations,
        top_x_percent,
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
    population = [Model() for _ in range(population_size)]
    print(f"Population before: {population}")
    for _ in tqdm.tqdm(range(num_generations), desc="generations", leave=False):
        # Evaluation
        for model in tqdm.tqdm(population, desc="model", leave=False):
            for t in tqdm.tqdm(range(num_tournaments), desc="tournament", leave=False):
                opponent = random.choice([e for e in population if e != model])
                inst = Game()
                inst.run(
                    players=[model, opponent], tournament_rounds=tournament_rounds)
        # Update the population
        # Selection
        num_replacements = math.floor(len(population)*top_x_percent)
        population = sorted(population, key=lambda x: x.bankroll, reverse=True)
        best_candidate = population[0]
        crossover_candidates = population[:num_replacements]
        # Removal
        for _ in range(num_replacements):
            population.pop()
        # Crossover
        for i in range(1, num_replacements):
            child = Model.generate_child(
                best_candidate, crossover_candidates[i])
            population.append(child)
        # Mutation
        for p in population:
            if random.random() < mutation_rate:
                p.mutate(mutation_volatility)

    # Return the best individual from the final population
    print(f"Population after: {population}")
    best_model = max(population, key=lambda x: x.bankroll)
    return best_model


if __name__ == '__main__':
    best_model = evolutionary_algorithm(
        population_size=4,
        num_generations=2,
        round_replacements=0.1,
        mutation_rate=0.05,
        mutation_volatility=0.1,
        num_tournaments=2,
        tournament_rounds=4
    )
    print(best_model)
