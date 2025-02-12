import pygame
from game import Game

def main():
    pygame.init()
    pygame.display.set_caption("Jaipur")

    game = Game()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(event.pos)

        game.draw()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
