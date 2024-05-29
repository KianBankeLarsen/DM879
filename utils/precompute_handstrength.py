import logging
import pickle
import eval7
from time import sleep
import concurrent.futures

from functools import partial


def simulate(cards, deck, n=1):
    """Simulates n games using the players cards by drawing
    random cards for the opponent and to finish the board.
    """
    cards = [deck[card] for card in cards]
    win = 0
    lose = 0
    draw = 0
    for i in range(n):
        deck = eval7.Deck()
        deck.shuffle()
        deck.cards = [card for card in deck.cards if card not in cards]
        opponent_cards = deck.deal(2)
        sampled_board_cards = deck.deal(7 - len(cards))
        player_score = eval7.evaluate(cards + sampled_board_cards)
        opponent_score = eval7.evaluate(opponent_cards + sampled_board_cards)
        if player_score > opponent_score:
            win += 1
        elif player_score < opponent_score:
            lose += 1
        else:
            draw += 1
    return win / n


def simulate_from_key(key, n=1000):
    """Simulates n games using the players cards by drawing
    random cards for the opponent and to finish the board.
    """
    # print(key)
    card_strs = key.split(',')
    cards = [eval7.Card(card) for card in card_strs]
    
    win = 0
    lose = 0
    draw = 0
    for i in range(n):
        deck = eval7.Deck()
        deck.shuffle()
        deck.cards = [card for card in deck.cards if card not in cards]
        opponent_cards = deck.deal(2)
        sampled_board_cards = deck.deal(7 - len(cards))
        player_score = eval7.evaluate(cards + sampled_board_cards)
        opponent_score = eval7.evaluate(opponent_cards + sampled_board_cards)
        if player_score > opponent_score:
            win += 1
        elif player_score < opponent_score:
            lose += 1
        else:
            draw += 1
    # print(f"key : {key}, win : {win / n}")
    return key, win / n

def rec_simulate_hand(deck, card_idxs, last_card_idx, n_cards, result_dict):
    if n_cards == 0:
        # print(f"card_idxs : {card_idxs}")
        # w_rate = simulate(card_idxs, deck, 1000)
        hand_key = ','.join(str(deck[c]) for c in card_idxs)
        # result_dict[hand_key] = w_rate
        result_dict[hand_key] = 0
        return
    
    for i in range(last_card_idx, 52):
        new_card_idxs = card_idxs.copy()
        new_card_idxs.append(i)
        rec_simulate_hand(deck, new_card_idxs, i + 1, n_cards - 1, result_dict)
        # print(f"in for loop n cards : {n_cards}, len of dict {len(result_dict)}: ")
    return result_dict

def simulate_hand_of_size(n_cards):
    deck = eval7.Deck()
    result_dict = {}
    result_dict = rec_simulate_hand(deck, [], 0, n_cards, result_dict)
    return result_dict

def simulate_all_hand_sizes():
    deck = eval7.Deck()
    result_dict = {}
    for n_cards in [2,5,6,7]:
        print("Simulating hands of size", n_cards, "...")
        res = simulate_hand_of_size(n_cards)
        result_dict.update(res)
    return result_dict


# Define the process_key function within the __main__ block
if __name__ == '__main__':
    # Your function definitions here...
    # Load or generate your data
    hand_size = 5
    d = simulate_hand_of_size(hand_size)
    keys = list(d.keys())
    print(keys)
    result = None
    
    # Example: processing smaller chunks of data to reduce memory usage
    with concurrent.futures.ProcessPoolExecutor() as executor:
        try:
            results = list(executor.map(simulate_from_key, keys, chunksize=100))
            print(results)
        except Exception as e:
            logging.error(f"Exception during parallel processing: {e}")
    
    # Filter out None values from results
    results = [result for result in results if result is not None]

    # Convert the results back into a dictionary
    new_data = dict(results)
    print(new_data)

    # Save the results to a file
    with open(f"precomputed_handstrength_{hand_size}_cards", "wb") as f:
        pickle.dump(new_data, f)

