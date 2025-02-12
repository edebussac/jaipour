import pygame
from constants import CARD_COLORS, TOKEN_VALUES, BLACK, small_font

class TokenPool:
    def __init__(self):
        self.pool = {k: v.copy() for k, v in TOKEN_VALUES.items()}

    def take_tokens(self, good_type, count):
        available = self.pool.get(good_type, [])
        if len(available) < count:
            taken = available[:count-1]
            self.pool[good_type] = available[count-1:]
            return taken
        taken = available[:count]
        self.pool[good_type] = available[count:]
        return taken

    def draw_tokens(self, screen):
        x, y = 1200, 100  # Position de départ pour les jetons
        radius = 20  # Rayon des cercles
        for good_type, values in self.pool.items():
            color = CARD_COLORS[good_type]
            for value in values:
                pygame.draw.circle(screen, color, (x, y), radius)
                text = small_font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)
                x -= 50  # Espacement entre les cercles
            y += 60  # Espacement entre les lignes
            x = 1200  # Réinitialiser la position x pour la ligne suivante
