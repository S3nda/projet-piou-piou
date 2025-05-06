import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')

class Target:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "target.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.math.Vector2(x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with(self, player_rect):
        return self.rect.colliderect(player_rect)