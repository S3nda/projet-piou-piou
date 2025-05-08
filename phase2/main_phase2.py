import pygame
from phase2.player import Player
from phase2.planet import Planet
from phase2.target import Target
import random

class Phase1:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.planets = []
        self.player = Player(self.width // 2, self.height - 100)
        self.target = Target(random.randint(200, self.width - 200), 100)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        # Génération des 3 planètes espacées
        while len(self.planets) < 3:
            new_planet = Planet.random(self.width, self.height)
            if all(p.distance_to(new_planet) > 200 for p in self.planets):
                self.planets.append(new_planet)

        while running:
            self.screen.fill((5, 5, 20))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                self.player.handle_input(event)

            self.player.update(self.planets)

            # Dessin
            self.target.draw(self.screen)
            for planet in self.planets:
                planet.draw(self.screen)

            self.player.draw(self.screen)

            # Victoire
            if self.target.collides_with(self.player):
                self.player.win_animation()
                pygame.display.flip()
                pygame.time.wait(1500)
                return "phase1"

            # Collision planète
            if any(planet.collides_with(self.player) for planet in self.planets):
                self.player.explode_animation()
                pygame.display.flip()
                pygame.time.wait(1500)
                return "menu"

            pygame.display.flip()
            clock.tick(60)