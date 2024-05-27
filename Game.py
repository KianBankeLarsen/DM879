from engine import Game
import players.interactivePlayer
import players.evolutionPlayer

game = Game()

player1 = players.interactivePlayer.Player()
player2 = players.interactivePlayer.Player()

ev = players.evolutionPlayer.EvolutionPlayer()
ev_player = ev.get_player("res/individual_49.pickle")
ev_player.bankroll = 0

tournament_rounds = 1
game.run([player1, ev_player], tournament_rounds)

print("Me:", player1.bankroll)
print("Bot:", ev_player.bankroll)

print("Opponent cards:", game.hands[1])

