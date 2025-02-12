import pygame

# Initialisation de Pygame
pygame.init()

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
GOLD = (255, 215, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Police
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Constantes du jeu
CARD_TYPES = ['Diamant', 'Or', 'Argent', 'Tissu', 'Épice', 'Cuir', 'Camel']
CARD_COLORS = {
    'Diamant': (0, 191, 255),
    'Or': (255, 215, 0),
    'Argent': (192, 192, 192),
    'Tissu': (255, 105, 180),
    'Épice': (139, 69, 19),
    'Cuir': (210, 180, 140),
    'Camel': (244, 164, 96)
}
TOKEN_VALUES = {
    'Diamant': [7, 7, 5, 5, 5],
    'Or': [6, 6, 5, 5, 5],
    'Argent': [5, 5, 5, 5, 5],
    'Tissu': [5, 3, 3, 2, 2, 1, 1],
    'Épice': [5, 3, 3, 2, 2, 1, 1],
    'Cuir': [4, 3, 2, 1, 1, 1, 1, 1, 1]
}
BONUS_VALUES = {
    '3': [1, 1, 2, 2, 3, 3, 2],
    '4': [4, 4, 5, 5, 6, 6],
    '5': [8, 8, 9, 10, 10]
}

# Configuration de la fenêtre
WIDTH, HEIGHT = 1300, 800
