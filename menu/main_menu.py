import pygame
import sys

class MenuPrincipal:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.options = ["Jouer", "Options", "Quitter"]
        self.selected = 0
        self.running = True
        self.choix_selectionne = None

    def afficher(self):
        self.screen.fill((30, 30, 30))
        for i, option in enumerate(self.options):
            couleur = (255, 255, 0) if i == self.selected else (255, 255, 255)
            texte = self.font.render(option, True, couleur)
            rect = texte.get_rect(center=(self.screen.get_width() // 2, 200 + i * 80))
            self.screen.blit(texte, rect)
        pygame.display.flip()

    def gerer_evenements(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.executer_selection()

    def executer_selection(self):
        choix = self.options[self.selected]
        if choix == "Jouer":
            self.choix_selectionne = "phase1"
            self.running = False
        elif choix == "Options":
            print("Menu des options (non implémenté)")
        elif choix == "Quitter":
            pygame.quit()
            sys.exit()

    def run(self):
        self.running = True
        self.choix_selectionne = None
        while self.running:
            self.gerer_evenements()
            self.afficher()
            self.clock.tick(60)
        return self.choix_selectionne
