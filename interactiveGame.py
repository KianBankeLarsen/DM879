from engine import Game
from players.interactivePlayer import Player

game = Game()

player1 = Player()
player2 = Player()
tournament_rounds = 1

game.run([player1, player2], tournament_rounds)
