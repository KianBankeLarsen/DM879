import eval7

def simulate_win_rate(round_state, active, n_simulations=100):
    """
    Makes n_simulations complete simulations from the given game and round state
    and returns a triple of the number of wins, loses and draws that result from 
    the simulations.
    """
    print("Simulating games...")
    player_cards = [eval7.Card(c) for c in round_state.hands[active]]
    board_cards = [eval7.Card(c) for c in round_state.deck[:round_state.street]]
    win = 0
    lose = 0
    draw = 0
    for _ in range(n_simulations):
        deck = eval7.Deck()
        deck.shuffle()
        deck.cards = [card for card in deck.cards if card not in player_cards + board_cards]
        opponent_cards = deck.deal(2)
        sampled_board_cards = deck.deal(5 - round_state.street)
        print(f"Opponent cards: {opponent_cards}")
        print(f"concatenation: {player_cards + board_cards + sampled_board_cards}")
        print(f"eval: {eval7.evaluate(player_cards + board_cards + sampled_board_cards)}")
        player_score = eval7.evaluate(player_cards + board_cards + sampled_board_cards)
        opponent_score = eval7.evaluate(opponent_cards + board_cards + sampled_board_cards)
        if player_score > opponent_score:
            win += 1
        elif player_score < opponent_score:
            lose += 1
        else:
            draw += 1
    return win, lose, draw