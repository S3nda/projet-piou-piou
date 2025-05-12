import pygame
import random
from phase2.utils import (
    distance,
    gravitational_force,
)  # Importation des fonctions utilitaires pour calculer la distance et la force gravitationnelle
import os


class Planet(pygame.sprite.Sprite):
    def __init__(
        self, position, mass, gravity_range, size, image_folder="../assets/planet/"
    ):
        super().__init__()  # Appel du constructeur de la classe parent Sprite de Pygame
        self.mass = mass  # Masse de la planète
        self.gravity_range = (
            gravity_range  # Plage de la zone d'influence gravitationnelle de la planète
        )
        self.size = size  # Taille de la planète donnée en paramètre

        # Sélection aléatoire d'une image parmi les fichiers .png dans le dossier spécifié
        planet_images = [
            f for f in os.listdir(image_folder) if f.endswith(".png")
        ]  # Récupération de tous les fichiers .png dans le dossier
        if not planet_images:  # Si aucun fichier image n'est trouvé
            raise FileNotFoundError(
                f"Aucune image trouvée dans le dossier {image_folder}"
            )  # Lève une exception si aucune image n'est disponible

        # Choix aléatoire d'une image
        chosen_image = random.choice(
            planet_images
        )  # Sélection aléatoire d'une image parmi celles disponibles
        self.original_image = pygame.image.load(
            os.path.join(image_folder, chosen_image)
        ).convert_alpha()  # Chargement de l'image choisie avec transparence

        # Redimensionnement de l'image selon la taille spécifiée pour la planète
        self.image = pygame.transform.scale(
            self.original_image, (self.size, self.size)
        )  # Redimensionne l'image de la planète
        self.rect = self.image.get_rect(
            center=position
        )  # Création du rectangle de collision autour de la planète

        # Position réelle de la planète pour les calculs physiques
        self.position = pygame.math.Vector2(position)

    def apply_gravity_to_player(self, player):
        """Applique la force gravitationnelle sur un joueur si celui-ci est dans la zone d'attraction de la planète."""
        # Calcul de la distance entre la planète et le joueur
        distance_to_player = self.position.distance_to(player.position)

        # Si le joueur est dans la zone d'attraction gravitationnelle de la planète
        if distance_to_player < self.gravity_range:
            # Calcul de la force gravitationnelle (en simplifiant la masse du joueur à 1)
            G = 6.67430e-11  # Constante gravitationnelle universelle
            force_magnitude = (
                (G * self.mass * 1) / (distance_to_player**2)
            )  # Force gravitationnelle calculée avec la formule de la gravité universelle

            # Direction de la gravité, un vecteur dirigé vers la planète
            gravity_direction = (
                self.position - player.position
            ).normalize()  # Normalisation du vecteur pour avoir une direction unitaire

            # Retourne la force gravitationnelle à appliquer au joueur
            return gravity_direction * force_magnitude
        return pygame.math.Vector2(
            0, 0
        )  # Si le joueur est hors de la zone de gravité, pas de force appliquée

    def draw(self, screen):
        """Affiche la planète  sur l'écran."""
        screen.blit(
            self.image, self.rect
        )  # Dessine l'image de la planète à la position définie par self.rect
