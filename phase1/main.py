import pygame
from phase1.player import Player
from phase1.rockspawner import RockSpawner
from phase1.enemy_spawner import EnemySpawner
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
        bg_path = os.path.join(ASSETS_DIR, "bg.png")
        self.background = pygame.image.load(bg_path).convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        self.player = Player(self.width // 2, self.height // 2 + 200, self.screen)
        self.rock_group = pygame.sprite.Group()
        self.rock_spawner = RockSpawner(screen, self.rock_group)
        self.spawner = EnemySpawner(screen)

        self.score = 0
        self.current_wave = 0
        self.max_waves = 9
        self.wave_completed = True
        self.wave_transition_timer = 0
        self.wave_transition_delay = 3000
        self.font = pygame.font.SysFont("Arial", 48)
        self.small_font = pygame.font.SysFont("Arial", 24)

        # Invincibility
        self.invincibility_duration = 2000  # 2 seconds
        self.invincibility_timer = 0

    def run(self, clock):
        running = True

        while running:
            dt = clock.tick(180)
            self.invincibility_timer += dt
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            if self.wave_completed:
                if self.current_wave >= self.max_waves:
                    return "phase 2"
                self.wave_transition_timer += dt
                if self.wave_transition_timer >= self.wave_transition_delay:
                    self.wave_transition_timer = 0
                    self.current_wave += 1
                    self.spawner.spawn_wave(self.current_wave)
                    self.wave_completed = False
            else:
                if len(self.spawner.enemies) == 0:
                    self.wave_completed = True

            self.screen.blit(self.background, (0, 0))
            self.player.handle_input(keys)
            self.player.update(dt)
            self.player.draw(self.screen)
            self.rock_spawner.update(dt)
            self.rock_group.update()
            self.rock_group.draw(self.screen)
            self.spawner.update(dt)
            self.spawner.draw(self.screen)

            position = (0, 0)
            if self.player.hp >= 3:
                image_hp = pygame.image.load("assets/Healthbar_3.png").convert_alpha()
            elif self.player.hp == 2:
                image_hp = pygame.image.load("assets/Healthbar_2.png").convert_alpha()
            elif self.player.hp == 1:
                image_hp = pygame.image.load("assets/Healthbar_1.png").convert_alpha()
            else:
                image_hp = pygame.image.load("assets/Healthbar_0.png").convert_alpha()

            self.screen.blit(image_hp, position)
            score_text = self.small_font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (0, self.height))

            if self.invincibility_timer >= self.invincibility_duration and self.player_got_hit():
                self.player.hp -= 1
                self.invincibility_timer = 0

            if self.enemy_got_hit():
                self.score += 100

            if self.wave_completed and self.current_wave < self.max_waves:
                wave_text = self.font.render(f"Vague {self.current_wave + 1} sur {self.max_waves}", True, (255, 255, 255))
                self.screen.blit(wave_text, (self.width // 2 - wave_text.get_width() // 2, self.height // 3))

                if self.current_wave > 0:
                    completed_text = self.small_font.render(f"Vague {self.current_wave} complétée!", True, (200, 255, 200))
                    self.screen.blit(completed_text, (self.width // 2 - completed_text.get_width() // 2, self.height // 3 + 60))
            elif not self.wave_completed:
                wave_text = self.small_font.render(f"Vague {self.current_wave}/{self.max_waves}", True, (200, 200, 255))
                self.screen.blit(wave_text, (200, 50))

            pygame.display.flip()

            if not self.player.alive:
                font = self.font
                petite_police = self.small_font

                overlay = font.render("GAME OVER", True, (255, 255, 255))
                self.screen.blit(overlay, (self.width // 2 - overlay.get_width() // 2, self.height // 2 - overlay.get_height() // 2))

                message = petite_police.render("Appuie sur une touche pour recommencer", True, (200, 200, 200))
                self.screen.blit(message, (self.width // 2 - message.get_width() // 2, self.height // 2 + 50))

                pygame.display.flip()

                waiting = True
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return "quit"
                        if event.type == pygame.KEYDOWN:
                            return "restart"

    def player_got_hit(self):
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

    def enemy_got_hit(self):
        hit = False
        for enemy in self.spawner.enemies:
            for bullet in self.player.bullets:
                if pygame.sprite.collide_rect(enemy, bullet):
                    enemy.take_damage(1)
                    hit = True
        return hit
