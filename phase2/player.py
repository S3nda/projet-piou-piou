import pygame
import os
import math
from phase2.utils import vec_length, vec_normalize, vec_add, vec_scale

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "player.png")).convert_alpha()
        self.explosion_image = pygame.image.load(os.path.join(ASSETS_DIR, "explosion.png")).convert_alpha()
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = 16
        self.dragging = False
        self.start_pos = pygame.Vector2()
        self.launch_velocity = pygame.Vector2()
        self.has_shot = False
        self.trajectory = []

    def handle_input(self, event):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and not self.has_shot:
            if vec_length(mouse_pos - self.pos) < 50:
                self.dragging = True
                self.start_pos = mouse_pos

        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.launch_velocity = self.start_pos - mouse_pos
            self.velocity = self.launch_velocity
            self.dragging = False
            self.has_shot = True
            self.trajectory = []

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.launch_velocity = self.start_pos - mouse_pos
            self.update_trajectory()

    def update_trajectory(self):
        self.trajectory = []
        pos = pygame.Vector2(self.pos)
        vel = pygame.Vector2(self.launch_velocity)

        for _ in range(50):
            gravity = pygame.Vector2(0, 0)
            # Planètes seront fournies dans update()
            self.trajectory.append(pos.xy)
            pos += vel * 0.1  # Simple approximation
            vel += gravity * 0.1  # gravity sera ajoutée dans update()

    def update(self, planets):
        if self.has_shot:
            gravity = pygame.Vector2(0, 0)
            for planet in planets:
                direction = planet.pos - self.pos
                distance = max(vec_length(direction), 5)
                force = planet.gravity_strength / (distance ** 1.2)
                gravity += vec_normalize(direction) * force

            self.velocity += gravity
            self.pos += self.velocity

    def draw(self, screen):
        # Rotation vers la trajectoire
        if self.velocity.length_squared() > 0:
            angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x))
        else:
            angle = 0

        rotated_img = pygame.transform.rotate(self.image, angle)
        rect = rotated_img.get_rect(center=self.pos)
        screen.blit(rotated_img, rect)

        # Trajectoire
        if self.dragging and not self.has_shot:
            pygame.draw.lines(screen, (200, 200, 255), False, self.trajectory, 2)

    def explode_animation(self):
        explosion = pygame.transform.scale(self.explosion_image, (40, 40))
        rect = explosion.get_rect(center=self.pos)
        pygame.display.get_surface().blit(explosion, rect)

    def win_animation(self):
        pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), self.pos, 25)

    def get_rect(self):
        return pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)
