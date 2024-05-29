# globals.py
import pickle
from eval7 import Deck
lookup_dict = {}
deck_order = {}


def initialize_lookup_dict():
    global lookup_dict
    with open("utils/precomputed_handstrength_2_cards", "rb") as f:
        lookup_dict = pickle.load(f)
        
    with open("utils/precomputed_handstrength_5_cards", "rb") as f:
        lookup_dict.update(pickle.load(f))
    
    deck = Deck()
    order = {}
    for i in range(len(deck)):
        order[str(deck[i])] = i
    
    global deck_order
    deck_order = order
    
def get_lookup_dict():
    return lookup_dict

def get_lookup_hand(round_state, active):
    player_cards = round_state.hands[active]
    board_cards = round_state.deck[:round_state.street]
    cards = sorted(player_cards + board_cards, key=lambda x: deck_order[str(x)])
    key = ','.join(str(card) for card in cards)
    return lookup_dict[key]