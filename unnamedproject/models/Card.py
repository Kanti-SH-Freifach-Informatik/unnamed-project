from enum import Enum
import random


class CardColor(Enum):
    RED = 'R'
    BLUE = 'B'
    GREEN = 'G'
    YELLOW = 'Y'


class CardValue(Enum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    SKIP = 10


class Card:

    def __init__(self, color=None, value=None, representation=None):
        if representation is None or len(representation) < 2:
            self.color = random.choice(
                list(CardColor)) if color is None else color
            self.value = random.choice(
                list(CardValue)) if value is None else value
        else:
            self.color = CardColor(representation[:1])
            self.value = CardValue(int(representation[1:]))

    def __repr__(self):
        return self.color.value + str(self.value.value)
