from evolution.Simulator import evolution
from players.evolutionPlayer import EvolutionPlayer

if __name__ == '__main__':

    player = EvolutionPlayer()
    population = player.evolve(
        population_size=50,
        num_generations=100,
        round_replacement_percentage=0.2,
        percentage_of_children=0.2,  # percentage of round_replacement_percentage individuals that are children, rest dies to epedemic, and is replaced by mutations of best individual
        mutation_rate=0.05,
        mutation_volatility=0.01,
        num_tournaments=3,
        tournament_rounds=100
    )

    best_individual = max(population.population, key=lambda x: x.bankroll)

    for idx, ind in enumerate(sorted(population.population, key=lambda x: x.bankroll)):
        player.save_player(f"pickle/individual_{idx}.pickle", ind)
