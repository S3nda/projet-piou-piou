import pygame
import os
from pygame.math import Vector2

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')

class Planet:
    def __init__(self, x, y, radius=75, gravity_strength=1200):
        self.pos = Vector2(x, y)
        self.radius = radius
        self.gravity_strength = gravity_strength

        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "planet.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_gravity_force(self, player_pos):
        direction = self.pos - player_pos
        distance = max(direction.length(), 5)
        force = self.gravity_strength / (distance ** 1.2)
        return direction.normalize() * force

    def collides_with(self, player_rect):
        # Circle-rect collision approximation
        closest_x = max(player_rect.left, min(self.pos.x, player_rect.right))
        closest_y = max(player_rect.top, min(self.pos.y, player_rect.bottom))
        dist = Vector2(closest_x, closest_y).distance_to(self.pos)
        return dist < self.radius