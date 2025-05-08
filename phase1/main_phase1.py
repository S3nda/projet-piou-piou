import pygame

class Phase1:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.planets = []