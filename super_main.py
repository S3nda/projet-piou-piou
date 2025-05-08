import pygame
import sys
from phase1.main_phase1 import Phase1
from phase2.main_phase2 import Phase2
from transition import Transition

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
BG_COLOR = (30, 30, 30)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Void Seekers")
    clock = pygame.time.Clock()

    transition = Transition(screen, duration=1.5, color=(0, 0, 0))
    current_phase = 2
    transitioning = False

    phase1 = Phase1(screen)
    phase2 = Phase2(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)

        if not transitioning:
            if current_phase == 2:
                result = phase2.run()
                if result == "phase1":
                    transitioning = True
                    current_phase = 1
                    transition.start()
            elif current_phase == 1:
                result = phase1.run()
                if result == "phase2":
                    transitioning = True
                    current_phase = 2
                    transition.start()

        if transitioning:
            transition.update()
            if not transition.is_active():
                transitioning = False

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()