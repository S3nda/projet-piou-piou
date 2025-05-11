import pygame
from utils import distance, gravitational_force  # Importation des fonctions utilitaires pour la distance et la gravité

class Target(pygame.sprite.Sprite):
    def __init__(self, position, mass, gravity_range, image_path):
        super().__init__()  # Appel au constructeur de la classe parent Sprite de Pygame
        self.mass = mass  # Masse de la planète cible
        self.gravity_range = gravity_range  # Plage de la zone d'attraction gravitationnelle de la planète
        
        # Chargement de l'image de la planète et redimensionnement selon la plage gravitationnelle
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Chargement de l'image avec transparence
        scale_factor = gravity_range / 100  # Calcul du facteur d'échelle basé sur la plage de gravité
        self.image = pygame.transform.scale(self.original_image, (int(80 * scale_factor), int(80 * scale_factor)))  # Redimensionnement de l'image en fonction du facteur d'échelle
        self.rect = self.image.get_rect(center=position)  # Création du rectangle de collision de la planète avec son centre à la position donnée
        
        # Position réelle de la planète pour les calculs physiques
        self.position = pygame.math.Vector2(position)

    def apply_gravity(self, player):
        """Applique la force gravitationnelle sur le joueur si celui-ci est dans le champ d'attraction."""
        player_pos = pygame.math.Vector2(player.rect.center)  # Position du joueur
        dist = distance(self.position, player_pos)  # Calcul de la distance entre la planète et le joueur
        
        # Si le joueur est dans la zone d'attraction gravitationnelle, appliquer la gravité
        if dist < self.gravity_range:
            # Calcul de la force gravitationnelle entre la planète et le joueur
            force = gravitational_force(self.mass, player.mass, self.position, player_pos, gravitational_constant=0.05)
            player.apply_force(force)  # Applique la force gravitationnelle au joueur

    def check_collision(self, player):
        """Vérifie si le joueur a atteint la cible (victoire)."""
        return self.rect.colliderect(player.rect)  # Vérifie si les rectangles de la cible et du joueur se superposent (collision)

    def draw(self, screen):
        """Affiche la planète cible sur l'écran."""
        screen.blit(self.image, self.rect)  # Dessine l'image de la planète à sa position sur l'écran