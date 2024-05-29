from players.randomPlayer import RandomPlayer
from players.pairSeekingPlayer import PairSeekingPlayer
from players.evolutionPlayer import EvolutionPlayer
from engine import Game
from os import walk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# Load the population
folder = "second_run_results/pickle"
files = next(walk(folder))[2]
players = []
evo_player = EvolutionPlayer()
for f in files:
    players.append(evo_player.get_player(f"{folder}/{f}"))
players.sort(key=lambda p: p.bankroll, reverse=True)
# players = players[:20]
bankrolls = [p.bankroll for p in players]

# Play games against a random and pairseeking player
game = Game()
bankrolls_random = []
bankrolls_pairseeker = []
for p in players:
    random_player = RandomPlayer()
    pair_player = PairSeekingPlayer()
    r_res = game.run([p, random_player], 100)[0]
    # p_res = game.run([p, pair_player], 100)[0]
    bankrolls_random.append(r_res)
    # bankrolls_pairseeker.append(p_res)

# Initialise dataframe
data = {
    'player': [f'player{i}' for i in range(len(players))],
    'score': bankrolls_random.sort()
}
df = pd.DataFrame(data)
# Normalize the scores
normalized_df = df.copy()
score_columns = ['score']

for column in score_columns:
    normalized_df[column] = (df[column] - df[column].mean()) / df[column].mean()

# Create box plots
plt.figure(figsize=(10, 6))
sns.barplot(x='player', y='score', hue='player', data=normalized_df)
plt.title('Normalized Difference of Scores Against Opponents')
plt.xlabel('')
plt.ylabel('Normalized Bankroll Score')
plt.legend(title='Player')
plt.xticks(rotation=45)
plt.show()

p = players[0]
df = pd.DataFrame(dict(
    r=[p.strength, p.deception, p.aggression, p.betting_mean, p.betting_std],
    theta=['Strength','Deception','Aggression',
           'Betting mean', 'Betting Deviation']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.show()
# fig.write_image("radar_chart.png")