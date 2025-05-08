import pygame

class Transition:
    def __init__(self, screen, duration=1.0, color=(0, 0, 0)):
        self.screen = screen
        self.duration = duration
        self.color = color
        self.alpha = 255
        self.surface = pygame.Surface(screen.get_size())
        self.surface.fill(self.color)
        self.active = False
        self.clock = pygame.time.Clock()

    def start(self):
        self.active = True
        self.alpha = 255

    def update(self):
        if self.active:
            delta = self.clock.tick() / 1000.0
            fade_speed = 255 / self.duration
            self.alpha -= int(fade_speed * delta)
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False
            self.surface.set_alpha(self.alpha)
            self.screen.blit(self.surface, (0, 0))

    def is_active(self):
        return self.active

    def reset(self):
        self.alpha = 255
        self.active = False
