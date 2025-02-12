from collections import defaultdict
from card import Card
import random
from constants import BONUS_VALUES


class Player:
    def __init__(self):
        self.hand = []
        self.camels = 0
        self.score = 0
        self.tokens = defaultdict(list)

    def take_cards(self, cards):
        for card in cards:
            if card.type == 'Camel':
                self.camels += 1
            else:
                self.hand.append(card)

    def sell_goods(self, good_type, token_pool):
        count = len([c for c in self.hand if c.type == good_type])
        if count < 2:
            return False

        tokens = token_pool.take_tokens(good_type, count)
        if not tokens:
            return False

        self.hand = [c for c in self.hand if c.type != good_type]
        self.score += sum(tokens)
        self.tokens[good_type].extend(tokens)

        # Ajouter le bonus
        bonus = random.choice(BONUS_VALUES.get(str(count), [0]))
        self.score += bonus
        return bonus
