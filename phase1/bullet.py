import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "bullet_player.png"))
        self.pos = pygame.Vector2(x, y)
        self.speed = pygame.Vector2(0, -5) + pygame.Vector2(0, -velocity_y)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += self.speed
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)


class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, velocity_y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "bullet_enemy.png"))
        self.image = pygame.transform.rotate(self.image, 180)

        self.pos = pygame.Vector2(x, y)
        self.speed = pygame.Vector2(0, 2) + pygame.Vector2(0, velocity_y)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += self.speed
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        # if self.rect.bottom < 0:
        #     self.kill()
        #

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)
