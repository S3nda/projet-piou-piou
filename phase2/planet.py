import pygame
import random
from utils import distance, gravitational_force
import os

class Planet(pygame.sprite.Sprite):
    def __init__(self, position, mass, gravity_range, size, image_folder="../assets/planet/"):
        super().__init__()
        self.mass = mass
        self.gravity_range = gravity_range
        self.size = size  # Taille passée en paramètre

        # Choix aléatoire d'une image parmi les fichiers du dossier planet
        planet_images = [f for f in os.listdir(image_folder) if f.endswith(".png")]
        if not planet_images:
            raise FileNotFoundError(f"Aucune image trouvée dans le dossier {image_folder}")

        # Sélection d'une image aléatoire
        chosen_image = random.choice(planet_images)
        self.original_image = pygame.image.load(os.path.join(image_folder, chosen_image)).convert_alpha()

        # Redimensionnement de l'image selon la taille choisie
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        self.rect = self.image.get_rect(center=position)
        
        # Position pour les calculs physiques
        self.position = pygame.math.Vector2(position)

    def apply_gravity_to_player(self, player):
        """Applique la force gravitationnelle à un joueur."""
        # Calcul de la distance entre la planète et le joueur
        distance_to_player = self.position.distance_to(player.position)

        # Si le joueur est dans la zone de gravité
        if distance_to_player < self.gravity_range:
            # Calcul de la force gravitationnelle (en simplifiant la masse du joueur à 1)
            G = 6.67430e-11  # Constante gravitationnelle
            force_magnitude = (G * self.mass * 1) / (distance_to_player ** 2)  # Force gravitationnelle

            # Direction de la gravité (vecteur vers la planète)
            gravity_direction = (self.position - player.position).normalize()

            # Appliquer la force à la vitesse du joueur
            return gravity_direction * force_magnitude
        return pygame.math.Vector2(0, 0)  # Pas de gravité si hors de la zone d'influence

    def draw(self, screen):
        """Affiche la planète et son champ gravitationnel."""
        # Affichage de la zone de gravité pour le feedback visuel
        screen.blit(self.gravity_circle, self.gravity_circle_rect)
        screen.blit(self.image, self.rect)