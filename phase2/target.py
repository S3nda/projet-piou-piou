import pygame
from phase2.utils import distance, gravitational_force  # Importation des fonctions utilitaires pour la distance et la gravité

class Target(pygame.sprite.Sprite):
    def __init__(self, position, mass, gravity_range, image_path):
        super().__init__()
        self.mass = mass
        self.gravity_range = gravity_range
        
        self.original_image = pygame.image.load(image_path).convert_alpha()
        scale_factor = gravity_range / 100
        self.image = pygame.transform.scale(self.original_image, (int(80 * scale_factor), int(80 * scale_factor)))
        self.rect = self.image.get_rect(center=position)
        
        self.position = pygame.math.Vector2(position)

    def apply_gravity(self, player):
        """Applique la force gravitationnelle sur le joueur si celui-ci est dans le champ d'attraction."""
        player_pos = pygame.math.Vector2(player.rect.center)
        dist = distance(self.position, player_pos)
        
        if dist < self.gravity_range:
            force = gravitational_force(self.mass, player.mass, self.position, player_pos, gravitational_constant=0.05)
            player.apply_force(force)

    def check_collision(self, player):
        """Vérifie si le joueur a atteint la cible (victoire)."""
        return self.rect.colliderect(player.rect)

    def draw(self, screen):
        """Affiche la planète cible sur l'écran."""
        screen.blit(self.image, self.rect)
