import pygame
import random
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")

class Planet(pygame.sprite.Sprite):
    def __init__(self, position, mass, gravity_range, size, image_folder=os.path.join(ASSETS_DIR, "planet")):
        super().__init__()
        self.mass = mass
        self.gravity_range = gravity_range
        self.size = size

        planet_images = [f for f in os.listdir(image_folder) if f.endswith(".png")]
        if not planet_images:
            raise FileNotFoundError(f"Aucune image trouvée dans le dossier {image_folder}")

        chosen_image = random.choice(planet_images)
        self.original_image = pygame.image.load(os.path.join(image_folder, chosen_image)).convert_alpha()

        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect(center=position)

        self.position = pygame.math.Vector2(position)

    def apply_gravity_to_player(self, player):
        """Applique la force gravitationnelle sur un joueur si celui-ci est dans la zone d'attraction de la planète."""
        distance_to_player = self.position.distance_to(player.position)

        if distance_to_player < self.gravity_range:
            G = 6.67430e-11
            force_magnitude = (G * self.mass * 4) / (distance_to_player ** 2)

            gravity_direction = (self.position - player.position).normalize()

            return gravity_direction * force_magnitude
        return pygame.math.Vector2(0, 0)

    def draw(self, screen):
        """Affiche la planète  sur l'écran."""
        screen.blit(self.image, self.rect)
