import pygame
from phase1.main import Phase1

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
phase = Phase1(screen)
phase.run()
pygame.quit()
