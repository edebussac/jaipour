import pygame
from constants import CARD_COLORS

class Card:
    def __init__(self, card_type):
        self.type = card_type
        self.color = CARD_COLORS[card_type]
        self.rect = pygame.Rect(0, 0, 54, 80)  # Nouvelles dimensions des cartes
