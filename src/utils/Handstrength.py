import eval7


def estimate_hand_strength(round_state, active, n=100):
    """Simulates n games using the players cards by drawing
    random cards for the opponent and to finish the board.
    """
    player_cards = round_state.hands[active]
    board_cards = round_state.deck[:round_state.street]
    win = 0
    lose = 0
    draw = 0
    for _ in range(n):
        deck = eval7.Deck()
        deck.shuffle()
        deck.cards = [
            card for card in deck.cards if card not in player_cards + board_cards]
        opponent_cards = deck.deal(2)
        sampled_board_cards = deck.deal(5 - round_state.street)
        player_score = eval7.evaluate(
            player_cards + board_cards + sampled_board_cards)
        opponent_score = eval7.evaluate(
            opponent_cards + board_cards + sampled_board_cards)
        if player_score > opponent_score:
            win += 1
        elif player_score < opponent_score:
            lose += 1
        else:
            draw += 1
    return win / n
