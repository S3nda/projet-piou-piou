import pygame
import os
import math
from phase1.utils import vec_length, vec_normalize, vec_add, vec_scale

ASSETS_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets')

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load(os.path.join(ASSETS_DIR, "player.png")).convert_alpha()
        self.explosion_image = pygame.image.load(os.path.join(ASSETS_DIR, "explosion.png")).convert_alpha()
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = 16 #à modifier potentiellement faut faire du playtest
        self.dragging = False #à retirer potentiellement
        self.start_pos = pygame.Vector2()
        self.launch_velocity = pygame.Vector2()
        self.has_shot = False
        self.trajectory = []

#mouvement zqsd définir vélocité, voir si accélération offshoot etc...
    def handle_input(self, event):
        key = pygame.key.get_pressed()
        if key[pygame.K_q] == True :
            player.move_ip(x_coord, y_coord)
        elif key[pygame.K_d] == True :
            player.move_ip(x_coord, y_coord)
        elif key[pygame.K_z] == True :
            player.move_ip(x_coord, y_coord)
        elif key[pygame.K_s] == True :
            player.move_ip(x_coord, y_coord)

#tirer == True quand [enter a key] est pressé
    def pioupiou_input(self, event):
        key = pygame.key.get_pressed()

#faire tirer le vaisseau
    def shoot():


    def explode_animation(self):
        explosion = pygame.transform.scale(self.explosion_image, (40, 40))
        rect = explosion.get_rect(center=self.pos)
        pygame.display.get_surface().blit(explosion, rect)

    def win_animation(self):
        pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), self.pos, 25)

    def get_rect(self):
        return pygame.Rect(self.pos.x - self.radius, self.pos.y - self.radius, self.radius * 2, self.radius * 2)