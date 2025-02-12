from deck import Deck
from card import Card

class Market:
    def __init__(self, deck):
        self.goods = []
        self.deck = deck
        self.initial_setup()

    def initial_setup(self):
        # Ajouter 3 chameaux
        camels = [c for c in self.deck.cards if c.type == 'Camel'][:3]
        for c in camels:
            self.deck.cards.remove(c)
        self.goods.extend(camels)

        # Ajouter 2 autres cartes
        goods = [c for c in self.deck.cards if c.type != 'Camel'][:2]
        for g in goods:
            self.deck.cards.remove(g)
        self.goods.extend(goods)

    def replenish(self):
        while len(self.goods) < 5 and self.deck.cards:
            card = self.deck.cards.pop(0)
            self.goods.append(card)
