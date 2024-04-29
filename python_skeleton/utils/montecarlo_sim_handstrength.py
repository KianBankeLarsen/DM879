from eval7 import Card, Deck, Evaluator

def simulate_win_rate(game_state, round_state, active, n_simulations=1000):
    """
    Simulate the win rate of active hand given the board cards
    """
    my_cards = round_state.hands[active]
    board_cards = round_state.deck[:round_state.street]
    
    for i in range(n_simulations):
        deck = Deck()
        deck.cards = [card for card in deck.cards if card not in my_cards + board_cards]
        opponent_cards = deck.deal(2)
        
        remaining_board_cards = deck.deal(5 - round_state.street)
        
        score_my = evaluator.evaluate(my_cards + board_cards + remaining_board_cards)
        
    