import pygame

from src.core.classes.game import Game
from src.core.classes.game_modes import Standard


# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()