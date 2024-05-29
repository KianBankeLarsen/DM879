import os
import pickle
from evolution.Simulator import evolution
from players.evolutionPlayer import EvolutionPlayer
from globals import initialize_lookup_dict, get_lookup_dict
from time import sleep
if __name__ == '__main__':
    
    initialize_lookup_dict()
    
    player = EvolutionPlayer()
    population = player.evolve(
        population_size=100,
        num_generations=10,
        round_replacement_percentage=0.1,
        percentage_of_children=0.5,  # percentage of round_replacement_percentage individuals that are children, rest dies to epedemic, and is replaced by mutations of best individual
        mutation_rate=0.05,
        mutation_volatility=0.02,
        num_tournaments=1,
        tournament_rounds=100
    )

    best_individual = max(population.population, key=lambda x: x.bankroll)

    for idx, ind in enumerate(sorted(population.population, key=lambda x: x.bankroll)):
        player.save_player(f"pickle/individual_{idx}.pickle", ind)


