import pygame
import random
import os
from phase2.player import Player
from phase2.planet import Planet
from phase2.target import Target

class Phase2Game:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_size()
        self.clock = pygame.time.Clock()
        self.FPS = 60

        background_folder = "assets/background/"
        background_images = [f for f in os.listdir(background_folder) if f.endswith(".png")]
        if not background_images:
            raise FileNotFoundError(f"Aucune image trouvée dans le dossier {background_folder}")
        
        chosen_background = random.choice(background_images)
        self.background = pygame.image.load(os.path.join(background_folder, chosen_background)).convert()
        self.background = pygame.transform.scale(self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.player = Player(
            position=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2),
            fuel=100,
            image_path="assets/player.png",
            explosion_path="assets/explosion.png"
        )

        self.target_planet = Target(
            position=(random.randint(200, 600), random.randint(100, 500)),
            mass=0.5,
            gravity_range=60,
            image_path="assets/target.png"
        )

        self.planets = self.generate_planets()

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.target_planet)
        self.all_sprites.add(*self.planets)

    def generate_planets(self):
        planets = []
        for _ in range(3):
            while True:
                pos = (random.randint(200, 800), random.randint(100, 600))
                if not self.is_planet_too_close(pos, planets) and not self.is_planet_on_player(pos, planets):
                    planet = Planet(
                        position=pos,
                        mass=random.randint(1, 3),
                        gravity_range=random.randint(200, 300),
                        size=random.choice([80, 100, 120])
                    )
                    planets.append(planet)
                    break
        return planets

    def is_planet_too_close(self, new_pos, planets):
        for planet in planets:
            if pygame.math.Vector2(new_pos).distance_to(planet.position) < (planet.rect.width / 2 + 100):
                return True
        if pygame.math.Vector2(new_pos).distance_to(self.target_planet.position) < (self.target_planet.rect.width / 2 + 100):
            return True
        return False

    def is_planet_on_player(self, new_pos, planets):
        if pygame.math.Vector2(new_pos).distance_to(self.player.position) < (self.player.rect.width / 2 + 100):
            return True
        if pygame.math.Vector2(new_pos).distance_to(self.target_planet.position) < (self.target_planet.rect.width / 2 + 100):
            return True
        return False

    def run(self):
        running = True
        last_time = pygame.time.get_ticks()

        while running:
            dt = pygame.time.get_ticks() - last_time
            last_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                self.player.handle_event(event)

            self.player.update(dt, self.planets)
            for planet in self.planets:
                planet.update(dt)

            if self.check_victory():
                print("Victoire ! Vous avez atteint la cible.")
                return "victory"
            if self.check_collision():
                self.player.explode()
                print("Perdu ! Vous avez percuté une planète obstacle.")
                return "defeat"

            self.screen.blit(self.background, (0, 0))
            self.all_sprites.draw(self.screen)
            self.player.draw_fuel_bar(self.screen)
            pygame.display.flip()
            self.clock.tick(self.FPS)

    def check_victory(self):
        distance = self.player.position.distance_to(self.target_planet.position)
        return distance < (self.player.rect.width / 2 + self.target_planet.rect.width / 2)

    def check_collision(self):
        for planet in self.planets:
            distance = self.player.position.distance_to(planet.position)
            if distance < (self.player.rect.width / 2 + planet.rect.width / 2):
                return True
        return False
