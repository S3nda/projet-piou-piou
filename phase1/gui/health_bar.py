import pygame
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "../..", "assets")
DEBUG = True

class HealthBar(pygame.sprite.Sprite):
    def __init__(self, player, position=(50, 50)):
        super().__init__()
        self.player = player  # Référence au joueur
        self.position = pygame.Vector2(position)
        self.image = None
        self.rect = None
        self.update()  # Charge l'image initiale

    def update(self):
        health = self.player.hp  # Accès à la vie du joueur

        # Choix de l'image en fonction de la vie
        if health >= 3:
            img_file = "Healthbar_3.png"
        elif health == 2:
            img_file = "Healthbar_2.png"
        elif health == 1:
            img_file = "Healthbar_1.png"
        else:
            img_file = "Healthbar_0.png"

        # Chargement de l'image
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, img_file)).convert_alpha()
        self.rect = self.image.get_rect(topleft=self.position)
