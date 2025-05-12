import pygame
import random
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, screen):
        super().__init__()
        self.screen = screen

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

        self.pos = pygame.Vector2(x, y)

        hitbox_width = 50 + 10 * scale_factor
        hitbox_height = 50 + 10 * scale_factor
        self.rect = pygame.Rect(0, 0, hitbox_width, hitbox_height)
        self.rect.center = (int(self.pos.x), int(self.pos.y))

        self.rotation_speed = self.speed * 0.05

    def update(self):
        self.pos.y += self.speed

        self.angle += self.rotation_speed
        if self.angle >= 360:
            self.angle -= 360

        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)

        if DEBUG:
            pygame.draw.rect(self.screen, (0, 255, 0), self.rect, 1)

        if self.rect.top > 1080:
            self.kill()
