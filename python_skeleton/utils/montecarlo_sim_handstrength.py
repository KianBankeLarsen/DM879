import eval7
import pickle

def simulate_win_rate(round_state, active, n_simulations=100):
    """
    Makes n_simulations complete simulations from the given game and round state
    and returns a triple of the number of wins, loses and draws that result from 
    the simulations.
    """
    # print("active : ", active)
    # print("hand : ", round_state.hands[active])
    # player_cards = [eval7.Card(c) for c in round_state.hands[active]]
    player_cards = round_state.hands[active]
    # board_cards = [eval7.Card(c) for c in round_state.deck[:round_state.street]]
    board_cards = round_state.deck[:round_state.street]
    win = 0
    lose = 0
    draw = 0
    for _ in range(n_simulations):
        deck = eval7.Deck()
        deck.shuffle()
        deck.cards = [card for card in deck.cards if card not in player_cards + board_cards]
        opponent_cards = deck.deal(2)
        sampled_board_cards = deck.deal(5 - round_state.street)
        player_score = eval7.evaluate(player_cards + board_cards + sampled_board_cards)
        opponent_score = eval7.evaluate(opponent_cards + board_cards + sampled_board_cards)
        if player_score > opponent_score:
            win += 1
        elif player_score < opponent_score:
            lose += 1
        else:
            draw += 1
    return win, lose, draw


def simulate(n_simulations, player_cards, suited = False):
    win = 0
    lose = 0
    draw = 0
    
    for _ in range(n_simulations):
        deck = eval7.Deck()
        deck.shuffle()
        opponent_cards = deck.deal(2)
        board_cards = deck.deal(5)
        player_score = eval7.evaluate(player_cards + board_cards + board_cards)
        opponent_score = eval7.evaluate(opponent_cards + board_cards + board_cards)

        if player_score > opponent_score:
            win += 1
        elif player_score < opponent_score:
            lose += 1
        else:
            draw += 1

    return win, lose, draw

non_pair_card_combinations = {"23": {"win":0, "lose":0, "draw":0}, "24": {"win":0, "lose":0, "draw":0}, "25": {"win":0, "lose":0, "draw":0}, "26": {"win":0, "lose":0, "draw":0}, "27": {"win":0, "lose":0, "draw":0}, "28": {"win":0, "lose":0, "draw":0}, "29": {"win":0, "lose":0, "draw":0}, "210": {"win":0, "lose":0, "draw":0}, "2J": {"win":0, "lose":0, "draw":0}, "2Q": {"win":0, "lose":0, "draw":0}, "2K": {"win":0, "lose":0, "draw":0}, "2A": {"win":0, "lose":0, "draw":0},
    "34": {"win":0, "lose":0, "draw":0}, "35": {"win":0, "lose":0, "draw":0}, "36": {"win":0, "lose":0, "draw":0}, "37": {"win":0, "lose":0, "draw":0}, "38": {"win":0, "lose":0, "draw":0}, "39": {"win":0, "lose":0, "draw":0}, "310": {"win":0, "lose":0, "draw":0}, "3J": {"win":0, "lose":0, "draw":0}, "3Q": {"win":0, "lose":0, "draw":0}, "3K": {"win":0, "lose":0, "draw":0}, "3A": {"win":0, "lose":0, "draw":0},
    "45": {"win":0, "lose":0, "draw":0}, "46": {"win":0, "lose":0, "draw":0}, "47": {"win":0, "lose":0, "draw":0}, "48": {"win":0, "lose":0, "draw":0}, "49": {"win":0, "lose":0, "draw":0}, "410": {"win":0, "lose":0, "draw":0}, "4J": {"win":0, "lose":0, "draw":0}, "4Q": {"win":0, "lose":0, "draw":0}, "4K": {"win":0, "lose":0, "draw":0}, "4A": {"win":0, "lose":0, "draw":0},
    "56": {"win":0, "lose":0, "draw":0}, "57": {"win":0, "lose":0, "draw":0}, "58": {"win":0, "lose":0, "draw":0}, "59": {"win":0, "lose":0, "draw":0}, "510": {"win":0, "lose":0, "draw":0}, "5J": {"win":0, "lose":0, "draw":0}, "5Q": {"win":0, "lose":0, "draw":0}, "5K": {"win":0, "lose":0, "draw":0}, "5A": {"win":0, "lose":0, "draw":0},
    "67": {"win":0, "lose":0, "draw":0}, "68": {"win":0, "lose":0, "draw":0}, "69": {"win":0, "lose":0, "draw":0}, "610": {"win":0, "lose":0, "draw":0}, "6J": {"win":0, "lose":0, "draw":0}, "6Q": {"win":0, "lose":0, "draw":0}, "6K": {"win":0, "lose":0, "draw":0}, "6A": {"win":0, "lose":0, "draw":0},
    "78": {"win":0, "lose":0, "draw":0}, "79": {"win":0, "lose":0, "draw":0}, "710": {"win":0, "lose":0, "draw":0}, "7J": {"win":0, "lose":0, "draw":0}, "7Q": {"win":0, "lose":0, "draw":0}, "7K": {"win":0, "lose":0, "draw":0}, "7A": {"win":0, "lose":0, "draw":0},
    "89": {"win":0, "lose":0, "draw":0}, "810": {"win":0, "lose":0, "draw":0}, "8J": {"win":0, "lose":0, "draw":0}, "8Q": {"win":0, "lose":0, "draw":0}, "8K": {"win":0, "lose":0, "draw":0}, "8A": {"win":0, "lose":0, "draw":0},
    "910": {"win":0, "lose":0, "draw":0}, "9J": {"win":0, "lose":0, "draw":0}, "9Q": {"win":0, "lose":0, "draw":0}, "9K": {"win":0, "lose":0, "draw":0}, "9A": {"win":0, "lose":0, "draw":0},
    "10J": {"win":0, "lose":0, "draw":0}, "10Q": {"win":0, "lose":0, "draw":0}, "10K": {"win":0, "lose":0, "draw":0}, "10A": {"win":0, "lose":0, "draw":0},
    "JQ": {"win":0, "lose":0, "draw":0}, "JK": {"win":0, "lose":0, "draw":0}, "JA": {"win":0, "lose":0, "draw":0},
    "QK": {"win":0, "lose":0, "draw":0}, "QA": {"win":0, "lose":0, "draw":0},
    "KA": 0
}

pair_card_combinations = {"22":{"win":0, "lose":0, "draw":0}, "33":{"win":0, "lose":0, "draw":0}, "44":{"win":0, "lose":0, "draw":0}, "55":{"win":0, "lose":0, "draw":0}, "66":{"win":0, "lose":0, "draw":0}, "77":{"win":0, "lose":0, "draw":0}, "88":{"win":0, "lose":0, "draw":0}, "99":{"win":0, "lose":0, "draw":0}, "1010":{"win":0, "lose":0, "draw":0}, "JJ":{"win":0, "lose":0, "draw":0}, "QQ":{"win":0, "lose":0, "draw":0}, "KK":{"win":0, "lose":0, "draw":0}, "AA":0}


def precompute_starting_hands(n_simulations=1000):
    suited_cards = non_pair_card_combinations
    non_suited_cards = non_pair_card_combinations + pair_card_combinations

    deck = eval7.Deck()

    for hand_key in suited_cards.keys():
        win, lose, draw = simulate(n_simulations, hand_key)
        suited_cards[hand_key]["win"] += win
        suited_cards[hand_key]["lose"] += lose
        suited_cards[hand_key]["draw"] += draw
        

    pass
    
    
    
    # Check for existing pkl
    # Add new results to existing results
    # Save results


