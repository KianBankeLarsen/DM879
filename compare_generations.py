from os import walk
import re
from engine import Game
from evolution.Individual import Individual
from globals import initialize_lookup_dict
from itertools import combinations


def find_best_in_generation(filename, generation):
    """Returns the best individual in the given generation"""
    f = open(filename)
    content = f.readlines()[0]
    content = content.split(", ")
    players = []
    for i in range(len(content)):
        e = content[i]
        s = float(re.search(r"Str:(\d+(?:\.\d+)?)", e).group(1))
        a = float(re.search(r"Agr:(\d+(?:\.\d+)?)", e).group(1))
        d = float(re.search(r"Dec:(\d+(?:\.\d+)?)", e).group(1))
        bem = float(re.search(r"BeM:(\d+(?:\.\d+)?)", e).group(1))
        bsd = float(re.search(r"BSD:(\d+(?:\.\d+)?)", e).group(1))
        br = int(re.search(r"BR:(-?\d+)", e).group(1))
        ind = Individual(strength=s, aggression=a, deception=d,
                         betting_mean=bem, betting_std=bsd, bankroll=0)
        players.append({"ind": ind, "generation": generation, "br": br})

    # Focus only on the 10 best
    players.sort(key=lambda p: p['br'], reverse=True)
    return {"ind": players[0]['ind'], "gen": players[0]['generation']}


if __name__ == "__main__":
    initialize_lookup_dict()
    the_elite = []
    folder = "generations/"
    files = next(walk(folder))[2]
    for f in files:
        gen = int(re.search(r"(\d+)", f).group(1))
        the_elite.append(find_best_in_generation(f"{folder}{f}", gen))

    game = Game()
    for e1, e2 in combinations(the_elite, 2):
        e1_bankroll = game.run([e1['ind'], e2['ind']], 500)[0]
        print(f"gen{e1["gen"]} vs gen{e2["gen"]} // ", end="")
        if e1_bankroll == 0:
            print("result was a draw")   
        else:
            winner = e1 if e1_bankroll > 0 else e2
            points = e1_bankroll if winner == e1 else -e1_bankroll
            print(f"winner was gen{winner["gen"]} with {points} units")
        
        e1["ind"].bankroll = 0
        e2["ind"].bankroll = 0
    
         


