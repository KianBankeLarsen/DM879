from engine import Game
from globals import initialize_lookup_dict
import players.interactivePlayer
import players.evolutionPlayer

game = Game()

player1 = players.interactivePlayer.Player()
ev = players.evolutionPlayer.EvolutionPlayer()

ev_player = ev.get_player("best_player.pickle")
ev_player.bankroll = 0
initialize_lookup_dict()
tournament_rounds = 1
game.run([player1, ev_player], tournament_rounds)

print("Me:", player1.bankroll)
print("Bot:", ev_player.bankroll)

print("Opponent cards:", game.hands[1])