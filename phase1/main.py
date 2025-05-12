import pygame
from phase1.player import Player
from phase1.rockspawner import RockSpawner
from phase1.enemy_spawner import EnemySpawner
from phase1.gui.health_bar import HealthBar
import os

### GLOBAL VAR ###
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


def clear_console():
    os.system("cls")


class Phase1:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()

        bg_path = os.path.join(ASSETS_DIR, "bg1.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(
            self.background, (self.width, self.height)
        )

        self.player = Player(self.width // 2, self.height // 2 + 200, self.screen)

        self.rock_group = pygame.sprite.Group()
        self.rock_spawner = RockSpawner(screen, self.rock_group)
        self.spawner = EnemySpawner(screen)

        self.health_bar = HealthBar(self.player)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        self.spawner.spawn_wave(2)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            dt = clock.tick(180)
            keys = pygame.key.get_pressed()

            self.screen.blit(self.background, (0, 0))

            self.player.handle_input(keys)
            self.player.update(dt)
            self.player.draw(self.screen)

            self.rock_spawner.update(dt)
            self.rock_group.update()
            self.rock_group.draw(self.screen)

            self.spawner.update(dt)
            self.spawner.draw(self.screen)

            self.health_bar.update()

            # Fonction qui vérifie les collisions
            if self.got_hit():
                self.player.hp -= 1

            pygame.display.flip()

            # Etat de game over
            # if self.player.death == True :
            #   overlay = font.render("GAME OVER", True, (255, 255, 255))
            #  screen.blit(overlay, (500, 500))

    #                message = petite_police.render("Appuie sur une touche pour recommencer", True, (200, 200, 200))
    #               screen.blit(message, (200, 350))

    def got_hit(self):
        for enemy in self.spawner.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                if DEBUG:
                    print("Vaisseau")
                return True
            for bullet in enemy.bullets:
                if pygame.sprite.collide_rect(self.player, bullet):
                    return True
        for rock in self.rock_group:
            if pygame.sprite.collide_rect(self.player, rock):
                return True
        return False
