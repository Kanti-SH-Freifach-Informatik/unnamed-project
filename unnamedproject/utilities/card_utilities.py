from random import random
from unnamedproject.models.Card import Card

def generate_hand(n_cards):
    cards = [] 
    for i in range (n_cards):
        cards.append(Card())
    return cards

def generate_hand_str(n_cards):
    cards = [str(c) for c in generate_hand(n_cards)] 
    return ",".join(cards) 

def parse_hand_str(hand):
    cards = hand.split(",")
    cards = [Card(c) for c in cards]
    return cards

