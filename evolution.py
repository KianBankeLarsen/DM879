import random
from DEFucked_engine import Game
from python_skeleton.model import Model


def evolutionary_algorithm(population_size, num_generations, mutation_chance, mutation_volatility, num_tournaments=5, tournament_rounds=1000):
    # Initialize population
    population = [Model() for _ in range(population_size)]
    
    for generation in range(num_generations):
        # Evaluation
        for model in population:
            for _ in range(num_tournaments):
                opponent = random.choice([e for e in population if e != model])
                inst = Game()
                result = inst.run(players=[model, opponent], tournament_rounds=tournament_rounds)
                print(f"model bankroll : {model.bankroll}")
                print(f"opponent bankroll : {opponent.bankroll}")
            # Play games and evaluate fitness
            # Update model's fitness attribute
            
        # Selection
        selected_parents = selection(population)
        
        # Crossover
        children = []
        for i in range(0, len(selected_parents), 2):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i+1]
            child = crossover(parent1, parent2)
            children.append(child)
        
        # Mutation
        for child in children:
            child.mutate(mutation_chance, mutation_volatility)
        
        # Replacement
        population = replacement(population, children)
    
    # Return the best individual from the final population
    best_model = max(population, key=lambda x: x.fitness)
    return best_model

def selection(population):
    # Implement selection method (e.g., tournament selection)
    pass

def crossover(parent1, parent2):
    # Implement crossover method (e.g., single-point crossover)
    pass

def replacement(population, children):
    # Implement replacement strategy
    pass

# Example usage
best_model = evolutionary_algorithm(population_size=100, num_generations=50, mutation_chance=0.05, mutation_volatility=0.1, num_tournaments=5, tournament_rounds=10)
