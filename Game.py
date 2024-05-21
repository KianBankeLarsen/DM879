from engine import Game
import players.interactivePlayer
import evolution.Individual

game = Game()

player1 = players.interactivePlayer.Player()
player2 = players.interactivePlayer.Player()

tournament_rounds = 1

game.run([player1, player2], tournament_rounds)
