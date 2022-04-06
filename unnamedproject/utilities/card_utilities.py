from random import random
from unnamedproject.models.Card import Card, CardColor, CardValue

def generate_hand(n_cards):
    cards = [] 
    for i in range (n_cards):
        cards.append(Card())
    return cards

def generate_hand_str(n_cards):
    cards = [str(c) for c in generate_hand(n_cards)] 
    return ",".join(cards)

def stringify_hand(hand):
    cards = [str(c) for c in hand] 
    return ",".join(cards)

def parse_hand_str(hand):
    cards = hand.split(",")
    cards = [Card(representation=c) for c in cards]
    return cards

def is_playable(top_card, next_card):
    a = next_card.color == top_card.color or next_card.value == top_card.value
    return a
