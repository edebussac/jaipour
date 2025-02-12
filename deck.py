import random
from card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        random.shuffle(self.cards)

    def create_deck(self):
        for _ in range(6): self.cards.append(Card('Diamant'))
        for _ in range(6): self.cards.append(Card('Or'))
        for _ in range(6): self.cards.append(Card('Argent'))
        for _ in range(8): self.cards.append(Card('Tissu'))
        for _ in range(8): self.cards.append(Card('Épice'))
        for _ in range(10): self.cards.append(Card('Cuir'))
        for _ in range(11): self.cards.append(Card('Camel'))
