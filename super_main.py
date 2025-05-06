import pygame
import sys

from menu.main_menu import Menu
from phase1.main_phase1 import Phase1
from phase2.main_phase2 import Phase2

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Super Game")

clock = pygame.time.Clock()
FPS = 60

# État actuel
state = "menu"

# Initialisation des scènes
menu = Menu(screen)
phase1 = Phase1(screen)
phase2 = Phase2(screen)

while True:
    if state == "menu":
        state = menu.run()
    elif state == "phase1":
        state = phase1.run()
    elif state == "phase2":
        state = phase2.run()
    elif state == "quit":
        pygame.quit()
        sys.exit()

    clock.tick(FPS)