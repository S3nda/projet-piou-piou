import pygame
import os
import math

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
DEBUG = True


class Starship(pygame.sprite.Sprite):
    def __init__(
        self, x, y, screen, image_path: str, fire_rate: int, direction: pygame.Vector2
    ):
        super().__init__()

        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)

        self.hp = 3
        self.bullets = pygame.sprite.Group()
        self.bullet_x = self.pos.x
        self.bullet_y = self.pos.y

        self.direction = direction

        if self.direction.length_squared() != 0:
            self.direction = self.direction.normalize()

        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.rotate_image(self.original_image, self.direction)

        self.explosion_images = [...]  # liste d'images
        self.explosion_index = 0
        self.explosion_timer = 0
        self.explosion_frame_duration = 130  # durée de chaque frame en ms
        self.dying = False
        self.alive = True

        explosion_image1 = pygame.image.load(
            os.path.join(ASSETS_DIR, "Explosion_animated", "Explosion_frame1.png")
        )
        explosion_image2 = pygame.image.load(
            os.path.join(ASSETS_DIR, "Explosion_animated", "Explosion_frame2.png")
        )
        explosion_image3 = pygame.image.load(
            os.path.join(ASSETS_DIR, "Explosion_animated", "Explosion_frame3.png")
        )
        explosion_image4 = pygame.image.load(
            os.path.join(ASSETS_DIR, "Explosion_animated", "Explosion_frame4.png")
        )
        explosion_image5 = pygame.image.load(
            os.path.join(ASSETS_DIR, "Explosion_animated", "Explosion_frame5.png")
        )
        explosion_image6 = pygame.image.load(
            os.path.join(ASSETS_DIR, "Explosion_animated", "Explosion_frame6.png")
        )

        self.explosion_images = [
            explosion_image1,
            explosion_image2,
            explosion_image3,
            explosion_image4,
            explosion_image5,
            explosion_image6,
        ]

        self.fire_rate = fire_rate
        self.fire_cooldown = 0

        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.hitbox = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.rect = self.hitbox

    def rotate_image(self, image, direction):
        angle = math.degrees(math.atan2(-direction.y, direction.x)) - 90
        return pygame.transform.rotate(image, angle)

    def update(self, dt):
        if not self.dying and self.alive:
            self.velocity.y = self.direction.y * self.velocity.y
            self.pos += self.velocity * 3  # mouvement libre dans le plan
            self.hitbox.center = (int(self.pos.x), int(self.pos.y))

            if self.hp <= 0:
                self.die()

            bullet_offset = (
                self.direction * 40
            )  # point de spawn dans la direction du vaisseau
            self.bullet_x = self.pos.x + bullet_offset.x
            self.bullet_y = self.pos.y + bullet_offset.y

            self.shoot(dt)
            self.bullets.update()
        elif self.dying:
            self.explosion_timer += dt
            if self.explosion_timer >= self.explosion_frame_duration:
                self.explosion_timer -= self.explosion_frame_duration
                self.explosion_index += 1
            if self.explosion_index < len(self.explosion_images):
                self.image = self.explosion_images[self.explosion_index]

    def draw(self, surface):
        image_rect = self.image.get_rect(center=self.hitbox.center)
        surface.blit(self.image, image_rect)
        self.bullets.draw(surface)

        if DEBUG:
            pygame.draw.rect(surface, (255, 0, 0), self.hitbox, 2)
            pygame.draw.circle(
                surface, (255, 0, 0), (int(self.bullet_x), int(self.bullet_y)), 5
            )

    def shoot(self, dt):
        pass  # à définir dans les sous-classes

    def die(self):
        if not self.dying:
            self.dying = True
            self.explosion_index = 0
            self.explosion_timer = 0
            self.image = self.explosion_images[0]
            self.alive = False
        self.kill()
        return 1
