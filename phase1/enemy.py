import pygame
import os
from phase1.starship import Starship
from phase1.bullet import EnemyBullet

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


class Enemy(Starship):
    def __init__(self, x, y, screen, instructions, health=1, fire_rate=800):
        image_path = os.path.join(ASSETS_DIR, "enemy.png")
        direction = pygame.Vector2(0, 1)  # vers le bas
        super().__init__(
            x, y, screen, image_path, fire_rate=fire_rate, direction=direction
        )
        """
        instructions look like [(velocity_vector, time_to_move, time_to_wait)]
        """
        self.hp = health
        self.instructions = instructions
        self.current_instruction = 0
        self.move_timer = 0
        self.wait_timer = 0
        self.is_moving = True
        self.is_waiting = False

    def update(self, dt):
        # Si nous sommes en attente, décrémenter le timer d'attente
        if self.is_waiting:
            self.wait_timer -= dt
            self.velocity = pygame.Vector2(0, 0)
            if self.wait_timer <= 0:
                self.is_waiting = False
                self.is_moving = True
                self.current_instruction = (self.current_instruction + 1) % len(
                    self.instructions
                )
                self.move_timer = 0
            return

        # Si nous sommes en mouvement
        if self.is_moving and self.current_instruction < len(self.instructions):
            velocity_vector, time_to_move, time_to_wait = self.instructions[
                self.current_instruction
            ]

            # Appliquer le vecteur de vélocité
            self.velocity = velocity_vector

            # Incrémenter le timer de mouvement
            self.move_timer += dt

            # Vérifier si le temps de mouvement est écoulé
            if self.move_timer >= time_to_move:
                self.is_moving = False
                self.is_waiting = True
                self.wait_timer = time_to_wait
                self.velocity = pygame.Vector2(0, 0)

        self.bullet_y = self.pos.y + 75
        super().update(dt)  # Appel à la méthode update de la classe parente

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
