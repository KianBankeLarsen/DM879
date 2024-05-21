import pickle
import evolution.Simulator
import evolution.Population


class EvolutionPlayer:
    def __init__(self):
        """
        Evolution player
        """
        pass

    def get_player(self, file: str) -> object:
        """
        Get a player object from Pickle
        """
        with open(file, "rb") as f:
            player = pickle.load(f)
        return player

    def save_player(self, file: str, player: object) -> None:
        """
        Save player object as Pickle
        """
        with open(file, "wb") as f:
            pickle.dump(player, f)

    def evolve(self, population_size,
               num_generations, 
               round_replacement_percentage, 
               percentage_of_children, 
               mutation_rate, 
               mutation_volatility, 
               num_tournaments, 
               tournament_rounds) -> evolution.Population:
        """
        Run evolution
        """
        return evolution.Simulator.evolution(
            population_size, 
            num_generations, 
            round_replacement_percentage, 
            percentage_of_children, 
            mutation_rate, 
            mutation_volatility, 
            num_tournaments,
            tournament_rounds)
