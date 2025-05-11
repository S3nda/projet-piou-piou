import pygame
import os
from phase1.bullet import PlayerBullet
from phase1.bullet import EnemyBullet
from phase1.starship import Starship

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


KEY_LEFT = pygame.K_LEFT
KEY_DOWN = pygame.K_DOWN
KEY_RIGHT = pygame.K_RIGHT
KEY_UP = pygame.K_UP


class Player(Starship):
    def __init__(self, x, y, screen):
        direction = pygame.Vector2(0, -1)  # vers le haut
        super().__init__(
            x,
            y,
            screen,
            os.path.join(ASSETS_DIR, "player.png"),
            fire_rate=100,
            direction=direction,
        )

    def handle_input(self, keys):
        self.velocity = pygame.Vector2(0, 0)
        if keys[KEY_LEFT]:
            self.velocity.x = -1
        if keys[KEY_RIGHT]:
            self.velocity.x = 1
        if keys[KEY_UP]:
            self.velocity.y = 1
        if keys[KEY_DOWN]:
            self.velocity.y = -1

        # normalisation
        if self.velocity.x != 0 and self.velocity.y != 0:
            self.velocity.x *= 0.7071
            self.velocity.y *= 0.7071

    def shoot(self, dt):
        if self.fire_cooldown <= 0:
            bullet = PlayerBullet(self.bullet_x, self.bullet_y, self.velocity.y)
            self.bullets.add(bullet)
            self.fire_cooldown = self.fire_rate
            if DEBUG:
                print("Player bullet tirée !", bullet.rect)
        else:
            self.fire_cooldown -= dt

    def update(self, dt):
        # on a besoin de limiter le vaisseau au bord, mais seulement quand il s'agit du joueur ( les enemis peuvent rester à l'exterieur de l'écran)
        self.pos.x = sorted((150, self.pos.x, self.screen_width - 150))[1]
        self.pos.y = sorted((75, self.pos.y, self.screen_height - 75))[1]
        return super().update(dt)
