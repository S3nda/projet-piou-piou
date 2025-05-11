import pygame
import os
from phase1.starship import Starship
from phase1.bullet import EnemyBullet

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


class Enemy(Starship):
    def __init__(self, x, y, screen, instructions=[], health=1, fire_rate=800):
        image_path = os.path.join(ASSETS_DIR, "enemy.png")
        direction = pygame.Vector2(0, 1)  # vers le bas
        super().__init__(
            x, y, screen, image_path, fire_rate=fire_rate, direction=direction
        )

        self.hp = health
        self.instructions = instructions
        self.current_instruction = 0
        self.instruction_timer = 0
        self.is_waiting = False
        self.wait_timer = 0

    def update(self, dt):
        if self.is_waiting:
            self.wait_timer -= dt
            self.velocity = pygame.Vector2(0, 0)
            if self.wait_timer <= 0:
                self.is_waiting = False
                self.current_instruction = (self.current_instruction + 1) % len(
                    self.instructions
                )
            return

        if self.current_instruction < len(self.instructions):
            dx, dy, wait_time = self.instructions[self.current_instruction]
            self.velocity.x = dx / 5
            self.velocity.y = -dy / 5
            self.instruction_timer += dt

            if self.instruction_timer >= 1000:
                target_x = self.pos.x + dx
                target_y = self.pos.y - dy
                distance = (
                    (target_x - self.pos.x) ** 2 + (target_y - self.pos.y) ** 2
                ) ** 0.5

                if distance < 10:
                    self.is_waiting = True
                    self.wait_timer = wait_time * 1000
                    self.instruction_timer = 0

        self.bullet_y = self.pos.y + 75
        super().update(dt)

    def shoot(self, dt):
        if self.fire_cooldown <= 0:
            bullet = EnemyBullet(self.bullet_x, self.bullet_y, self.velocity.y)
            self.bullets.add(bullet)
            self.fire_cooldown = self.fire_rate
            if DEBUG:
                print("Enemy bullet tirée !", bullet.rect)
        else:
            self.fire_cooldown -= dt

    def take_damage(self, damage=1):
        self.hp -= damage
        return self.hp <= 0
