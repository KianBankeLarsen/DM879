from globals import initialize_lookup_dict
from players.randomPlayer import RandomPlayer
from players.pairSeekingPlayer import PairSeekingPlayer
from evolution.Individual import Individual
from engine import Game
from os import walk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import re


def create_plot(data, opponent_type):
    """Creates bar plots for the given result data"""
    print(opponent_type)
    print(df)
    print()
    df = pd.DataFrame(data)
    # Normalizing the scores
    normalized_df = df.copy()
    # score_columns = ['score']
    # normalized_df['score'] = (
    #     df['score'] - df['score'].mean()) / df['score'].mean()
    normalized_df = normalized_df.sort_values(by=['score'])
    # Creating box plots
    plt.figure(figsize=(10, 6))
    sns.barplot(x='player', y='score', hue='player', data=normalized_df)
    plt.title(f'Scores Against {opponent_type}')
    plt.xlabel('')
    plt.ylabel('Bankroll')
    plt.legend(title='Player')
    plt.xticks(rotation=45)
    plt.show()


def create_radar_chart(players, trait):
    """Creates a radar chart over the attributes of the individual whom did best against
    the opponnent whom played with the given trait
    """
    players.sort(key=lambda p: p[trait], reverse=True)
    p = players[0]['ind']
    df = pd.DataFrame(dict(
        r=[p.strength, p.deception, p.aggression, p.betting_mean, p.betting_std],
        theta=['Strength', 'Deception', 'Aggression',
               'Betting mean', 'Betting Deviation']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    fig.show()
    fig.write_image(f"best_against_{trait}.png")


# Load the population
players = []
# From pickle files
# folder = "second_run_results/pickle"
# files = next(walk(folder))[2]
# evo_player = EvolutionPlayer()
# for f in files:
#     players.append(evo_player.get_player(f"{folder}/{f}"))

# From log file
f = open("result")
content = f.readlines()[0]
content = content.split(", ")
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
    players.append({"ind": ind, "against_random": 0,
                   "against_pair": 0, "against_population": br, "id": i})

## Focus only on the 10 best
players.sort(key=lambda p: p['against_population'], reverse=True)
players = players[:20]
for p in players:
    print(p)

# Playing games against a random or pairseeking player
initialize_lookup_dict()
game = Game()
for p in players:
    random_player = RandomPlayer()
    pair_player = PairSeekingPlayer()
    r_res = game.run([p['ind'], random_player], 1000)[0]
    p_res = game.run([p['ind'], pair_player], 1000)[0]
    p['against_random'] = r_res
    p['against_pair'] = p_res

# Plot results against random player
players.sort(key=lambda p: p['against_random'], reverse=True)
data = {
    'player': [f'player{p['id']}' for p in players],
    'score': [p['against_random'] for p in players]
}
create_plot(data, "RANDOM")

# Plot resulst against pair seeker
players.sort(key=lambda p: p['against_pair'], reverse=True)
data = {
    'player': [f'player{p['id']}' for p in players],
    'score': [p['against_pair'] for p in players]
}
create_plot(data, "PAIR_SEEKER")

# Plot resulst against population
players.sort(key=lambda p: p['against_population'], reverse=True)
data = {
    'player': [f'player{p['id']}' for p in players],
    'score': [p['against_population'] for p in players]
}
create_plot(data, "POPULATION")

create_radar_chart(players, 'against_random')
create_radar_chart(players, 'against_pair')
create_radar_chart(players, 'against_population')
