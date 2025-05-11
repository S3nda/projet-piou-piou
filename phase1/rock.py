import pygame
import random
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load(
            os.path.join(ASSETS_DIR, "rock.png")
        ).convert_alpha()
        self.speed = 1 + random.randint(0, 2)

        scale_factor = 0.4 + self.speed * 0.4
        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)
        self.original_image = pygame.transform.scale(
            self.original_image, (new_width, new_height)
        )

        self.angle = random.randint(0, 360)
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(x, y)

        self.rotation_speed = self.speed * 0.05

    def update(self):
        self.pos.y += self.speed

        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle -= 360

        self.image = pygame.transform.rotate(self.original_image, self.angle)

        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y = int(self.pos.y)

        if self.rect.top > 1080:  # à adapter à la hauteur de ton écran
            self.kill()
