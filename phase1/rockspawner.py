import pygame
import random
from phase1.rock import Rock  # adapte ce chemin si besoin


class RockSpawner:
    def __init__(self, screen, enemy_group, min_delay=300, max_delay=1500):
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.enemy_group = enemy_group
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.timer = 0
        self.next_spawn_time = random.randint(self.min_delay, self.max_delay)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.next_spawn_time:
            self.spawn_rock()
            self.timer = 0
            self.next_spawn_time = random.randint(self.min_delay, self.max_delay)

    def spawn_rock(self):
        x = random.randint(350, self.screen_width - 350)  # 100 = largeur max du rock
        rock = Rock(x, -40, self.screen)  # commence hors écran en haut
        self.enemy_group.add(rock)
