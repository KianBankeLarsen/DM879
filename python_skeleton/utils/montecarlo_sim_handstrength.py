import eval7

def simulate_win_rate(game_state, round_state, active, n_simulations=1000):
    """
    Simulate the win rate of active hand given the board cards
    """
    print("HERE")
    my_cards = round_state.hands[active]
    board_cards = round_state.deck[:round_state.street]
    
    my_win = 0
    opp_win = 0
    draw = 0
    
    for i in range(n_simulations):
        deck = eval7.Deck()
        deck.cards = [card for card in deck.cards if card not in my_cards + board_cards]
        opponent_cards = deck.deal(2)
        
        remaining_board_cards = deck.deal(5 - round_state.street)
        
        score_my = eval7.evaluate(my_cards + board_cards + remaining_board_cards)
        score_opp = eval7.evaluate(opponent_cards + board_cards + remaining_board_cards)
        
        if score_my > score_opp:
            my_win += 1
        elif score_my < score_opp:
            opp_win += 1
        else:
            draw += 1
    
    return (my_win, opp_win, draw)