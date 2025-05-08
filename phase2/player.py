import pygame
import os
import math
from phase2.utils import distance, normalize

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
        self.fuel = 100  # Ajout du système de carburant
        self.max_fuel = 100
        self.fuel_consumption_rate = 0.05  # Consommation par unité de distance

    def handle_input(self, event):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONDOWN and not self.has_shot and self.fuel > 0:
            if distance(mouse_pos, self.pos) < 50:
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
            self.trajectory.append(pos.xy)
            pos += vel * 0.1
            vel += gravity * 0.1

    def update(self, planets):
        if self.has_shot and self.fuel > 0:
            gravity = pygame.Vector2(0, 0)
            for planet in planets:
                direction = planet.pos - self.pos
                dist = max(distance(self.pos, planet.pos), 5)
                force = planet.gravity_strength / (dist ** 1.2)
                gravity += pygame.Vector2(normalize(direction)) * force

            self.velocity += gravity
            self.pos += self.velocity

            # Consommer du carburant
            self.fuel -= self.velocity.length() * self.fuel_consumption_rate
            self.fuel = max(self.fuel, 0)  # Ne pas descendre en dessous de zéro

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

        # Barre de carburant
        fuel_bar_width = 100
        fuel_bar_height = 10
        fuel_ratio = self.fuel / self.max_fuel
        fuel_color = (0, 255, 0) if fuel_ratio > 0.3 else (255, 0, 0)
        fuel_rect = pygame.Rect(self.pos.x - fuel_bar_width // 2, self.pos.y - 40, int(fuel_bar_width * fuel_ratio), fuel_bar_height)
        bg_rect = pygame.Rect(self.pos.x - fuel_bar_width // 2, self.pos.y - 40, fuel_bar_width, fuel_bar_height)
        pygame.draw.rect(screen, (50, 50, 50), bg_rect)
        pygame.draw.rect(screen, fuel_color, fuel_rect)

    def explode_animation(self):
        explosion = pygame.transform.scale(self.explosion_image, (40, 40))
        rect = explosion.get_rect(center=self.pos)
        pygame.display.get_surface().blit(explosion, rect)

    def win_animation(self):
        pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), self.pos, 25)

    def get_rect(self):
        return pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)