import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, position, fuel, image_path, explosion_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)
        
        # Position du joueur
        self.position = pygame.math.Vector2(position)
        
        # Vitesse initiale
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Carburant
        self.fuel = fuel
        self.fuel_max = fuel
        
        # Explosion
        self.explosion_image = pygame.image.load(explosion_path).convert_alpha()
        self.exploded = False
        
        # Rotation
        self.angle = 0  # Initialisation de l'angle (le vaisseau est orienté vers le haut)
        
        # Ajout de l'état de drag
        self.dragging = False
        
        # Taux de consommation de carburant
        self.fuel_consume_rate = 0.01  # Consommation minimale par pixel
        self.fuel_drain_factor = 0.1  # Facteur de drainage de carburant en fonction de la vitesse

        # Gravité
        self.gravity_strength = 0.1  # Force de gravité de la planète
        self.gravity_range = 200  # Plage de la gravité de la planète (en pixels)

    def update(self, dt, planets):
        """Met à jour la position et l'état du vaisseau"""
        if self.fuel > 0 and not self.dragging:  # Le vaisseau ne se déplace pas pendant le drag
            self.position += self.velocity * dt  # Déplace le vaisseau avec la vélocité
            self.rect.center = (int(self.position.x), int(self.position.y))
        
            # Consommation de carburant
            self.fuel -= self.velocity.length() * self.fuel_drain_factor * dt  # Drainage basé sur la vitesse
            self.fuel = max(self.fuel, 0)  # Ne pas avoir un carburant négatif

        # Applique la gravité des planètes
        self.apply_gravity(planets)

        # Applique la rotation en fonction de l'angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Assure que le centre du vaisseau reste au même endroit
    
    def apply_gravity(self, planets):
        """Applique la gravité des planètes sur le vaisseau."""
        total_gravity_force = pygame.math.Vector2(0, 0)  # Force gravitationnelle totale

        # Appliquer la gravité de chaque planète
        for planet in planets:
            gravity_force = planet.apply_gravity_to_player(self)
            total_gravity_force += gravity_force  # On additionne la gravité de chaque planète

        # Applique la force gravitationnelle totale à la vitesse du joueur
        self.velocity += total_gravity_force

    def handle_event(self, event):
        """Gère les événements du jeu (clavier, souris, etc.)"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Si on clique avec le bouton gauche
                self.dragging = True
                self.drag_start_pos = pygame.math.Vector2(event.pos)  # Position initiale du drag
                self.initial_angle = self.angle  # Sauvegarde l'angle initial avant le drag
                self.initial_position = self.position  # Sauvegarde la position du vaisseau
                self.velocity = pygame.math.Vector2(0, 0)  # Réinitialise la vitesse pendant le drag
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Calcul de l'angle par rapport à la souris (direction opposée)
                mouse_pos = pygame.math.Vector2(event.pos)
                direction_vector = mouse_pos - self.position
                direction_vector = -direction_vector  # Inverse la direction pour obtenir l'orientation correcte
                self.angle = math.degrees(math.atan2(-direction_vector.y, -direction_vector.x))
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center=self.rect.center)
                
                # Calcul de la vitesse pendant le drag (pas de consommation pendant le drag)
                drag_distance = direction_vector.length()
                self.velocity = direction_vector.normalize() * drag_distance * 0.001  # Ajuste la vitesse pendant le drag

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Quand on relâche le bouton gauche
                self.dragging = False
                self.launch_velocity = self.velocity  # La vitesse à laquelle le vaisseau est lancé après le drag
        
    def explode(self):
        """Gère l'explosion du vaisseau"""
        self.exploded = True
        self.image = self.explosion_image  # Affiche l'image d'explosion
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def move(self):
        """Déplace le vaisseau pendant le jeu"""
        if not self.dragging:  # Si le vaisseau n'est plus en train de draguer
            if self.fuel > 0:
                # Mise à jour de la position selon la vitesse
                self.position += self.velocity
                self.rect.center = (int(self.position.x), int(self.position.y))

    def draw_fuel_bar(self, screen):
        """Dessine la barre de carburant en haut de l'écran avec le texte 'Carburant'."""
        fuel_width = 1000
        fuel_height = 60
        fuel_percentage = self.fuel / self.fuel_max

        # Récupère la largeur de l'écran
        screen_width = screen.get_width()

        # Dessiner l'arrière-plan de la barre de carburant
        pygame.draw.rect(screen, (50, 50, 50), (screen_width // 2 - fuel_width // 2, 40, fuel_width, fuel_height))

        # Dessiner la barre de carburant
        pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - fuel_width // 2, 40, int(fuel_width * fuel_percentage), fuel_height))

        # Dessiner le texte "Carburant"
        font = pygame.font.SysFont("Arial", 40)
        text_surface = font.render("Carburant", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2, 70))
        screen.blit(text_surface, text_rect)