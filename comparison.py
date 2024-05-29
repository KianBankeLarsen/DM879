from players.randomPlayer import RandomPlayer
from players.pairSeekingPlayer import PairSeekingPlayer
from players.evolutionPlayer import EvolutionPlayer
from engine import Game
from os import walk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the population
folder = "res"
files = next(walk(folder))[2]
players = []
evo_player = EvolutionPlayer()
for f in files:
    players.append(evo_player.get_player(f"{folder}/{f}"))
players.sort(key=lambda p: p.bankroll, reverse=True)
# players = players[:10]
bankrolls = [p.bankroll for p in players]

# Play games against a random and pairseeking player
game = Game()
bankrolls_random = []
bankrolls_pairseeker = []
for p in players:
    random_player = RandomPlayer()
    pair_player = PairSeekingPlayer()
    r_res = game.run([p, random_player], 1)[0]
    p_res = game.run([p, pair_player], 100)[0]
    bankrolls_random.append(r_res)
    bankrolls_pairseeker.append(p_res)


data = {
    'player': [f'player{i}' for i in range(len(players))],
    'score_against_population': bankrolls_pairseeker
}

df = pd.DataFrame(data)

# Normalize the scores
normalized_df = df.copy()
score_columns = ['score_against_population']

for column in score_columns:
    normalized_df[column] = (df[column] - df[column].mean()) / df[column].mean()

print(normalized_df)
# Create box plots
plt.figure(figsize=(10, 6))
sns.barplot(x='player', y='score_against_population', hue='player', data=normalized_df)
plt.title('Normalized Difference of Scores Against Opponents')
plt.xlabel('')
plt.ylabel('Normalized Score')
plt.legend(title='Player')
plt.show()