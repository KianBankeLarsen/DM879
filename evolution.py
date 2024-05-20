import math
import random

import tqdm
from DEFucked_engine import Game
from python_skeleton.model import Model

def evolutionary_algorithm(population_size, num_generations, top_x_percent, mutation_chance, mutation_volatility, num_tournaments=5, tournament_rounds=1000):
    # Initialize population
    population = [Model() for _ in range(population_size)]
    
    for _ in tqdm.tqdm(range(num_generations), desc="generations", leave=False):
        # Evaluation
        for model in tqdm.tqdm(population, desc="model", leave=False):
            for t in tqdm.tqdm(range(num_tournaments), desc="tournament", leave=False):
                opponent = random.choice([e for e in population if e != model])
                inst = Game()
                inst.run(
                    players=[model, opponent], tournament_rounds=tournament_rounds)
                # print(f"model bankroll : {model.bankroll}")
                # print(f"opponent bankroll : {opponent.bankroll}")
            # Play games and evaluate fitness
            # Update model's fitness attribute

        # Selection
        selected_parents = selection(population, top_x_percent)

        # Crossover
        children = []
        for i in range(0, len(selected_parents), 2):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i+1]
            child = Model.generate_child(parent1, parent2)
            children.append(child)

        # Replacement (implicitly removed the worst individuals from the population)
        population = selected_parents + children
        print("mutation")
        # Mutation
        for model in population:
            model.mutate(mutation_chance, mutation_volatility)

    # Return the best individual from the final population
    best_model = max(population, key=lambda x: x.bankroll)
    return best_model

def selection(population, top_x_percent):
    lst = sorted(population, key=lambda x: x.bankroll, reverse=True)
    lst = lst[:math.floor(len(lst)*top_x_percent)]
    return lst


if __name__ == '__main__':
    best_model = evolutionary_algorithm(
        population_size=4, 
        num_generations=2, 
        top_x_percent=0.1,
        mutation_chance=0.05, 
        mutation_volatility=0.1, 
        num_tournaments=2, 
        tournament_rounds=4
    )
    print(best_model)