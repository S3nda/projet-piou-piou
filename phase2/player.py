import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, position, fuel, image_path, explosion_path):
        super().__init__()  # Initialisation de la classe parent Sprite de Pygame
        self.original_image = pygame.image.load(image_path).convert_alpha()  # Chargement de l'image du vaisseau
        self.image = self.original_image  # L'image actuelle du vaisseau
        self.rect = self.image.get_rect(center=position)  # Création du rectangle pour la collision avec le centre à la position donnée
        
        # Position du joueur (utilisation de Vector2 pour une gestion facile des coordonnées)
        self.position = pygame.math.Vector2(position)
        
        # Initialisation de la vitesse du joueur
        self.velocity = pygame.math.Vector2(0, 0)
        
        # Gestion du carburant
        self.fuel = fuel
        self.fuel_max = fuel  # Le carburant maximum que le vaisseau peut avoir
        
        # Explosion du vaisseau (chargement de l'image d'explosion)
        self.explosion_image = pygame.image.load(explosion_path).convert_alpha()
        self.exploded = False  # Variable pour suivre l'état d'explosion
        
        # Rotation du vaisseau
        self.angle = 0  # Initialisation de l'angle (le vaisseau est orienté vers le haut)
        
        # Etat de glissement (drag)
        self.dragging = False
        
        # Taux de consommation de carburant
        self.fuel_consume_rate = 0.01  # Consommation de carburant par pixel
        self.fuel_drain_factor = 0.1  # Facteur de drainage du carburant en fonction de la vitesse

        # Gravité
        self.gravity_strength = 0.1  # Force de la gravité exercée par la planète
        self.gravity_range = 200  # Plage d'attraction de la gravité (en pixels)

        # Limiter à un seul lancement
        self.has_launched = False


    def update(self, dt, planets):
        """Met à jour la position et l'état du vaisseau"""
        if self.fuel > 0 and not self.dragging:  # Si il y a du carburant et que le vaisseau n'est pas en train de glisser
            self.position += self.velocity * dt  # Déplacement du vaisseau en fonction de sa vitesse et du temps écoulé
            self.rect.center = (int(self.position.x), int(self.position.y))  # Mise à jour du centre du rectangle pour le déplacement
        
            # Consommation de carburant en fonction de la vitesse
            self.fuel -= self.velocity.length() * self.fuel_drain_factor * dt  # Dépense de carburant basée sur la vitesse
            self.fuel = max(self.fuel, 0)  # Le carburant ne peut pas être négatif

        # Applique la gravité des planètes
        self.apply_gravity(planets)

        # Applique la rotation en fonction de l'angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Assure que le centre reste fixe lors de la rotation
    
    def apply_gravity(self, planets):
        """Applique la gravité des planètes sur le vaisseau."""
        total_gravity_force = pygame.math.Vector2(0, 0)  # Initialisation de la force gravitationnelle totale

        for planet in planets:
            # Calcul de la distance entre la planète et le vaisseau
            dx = planet.position.x - self.position.x
            dy = planet.position.y - self.position.y
            distance = math.sqrt(dx**2 + dy**2)
            
            # Zone d'attraction (3 fois la taille de la planète)
            zone_attraction = (planet.rect.width / 2) * 3
            
            if distance < zone_attraction:  # Si le vaisseau est dans la zone d'attraction
                # Calcul de la force gravitationnelle avec un facteur de réduction
                force_magnitude = 100 / (distance ** 1.8)  # Réduit la force gravitationnelle avec une exponentiation modifiée
                
                # Réduction de la force pour un effet plus doux
                force_reduction_factor = 0.1  # Réduction de la force à 10% de sa valeur
                force_magnitude *= force_reduction_factor  # Application de la réduction
                
                # Direction de la gravité
                force_direction = pygame.math.Vector2(dx, dy).normalize()  # Normalisation pour obtenir la direction
                
                # Calcul de la force gravitationnelle
                gravity_force = force_direction * force_magnitude
                
                # Ajout de cette force à la force gravitationnelle totale
                total_gravity_force += gravity_force

        # Application de la force gravitationnelle totale à la vitesse du joueur
        self.velocity += total_gravity_force

    def handle_event(self, event):
        """Gère les événements du jeu (clavier, souris, etc.)"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.has_launched:  # Un seul lancement autorisé
                self.dragging = True
                self.drag_start_pos = pygame.math.Vector2(event.pos)  # Sauvegarde de la position initiale du drag
                self.initial_angle = self.angle  # Sauvegarde de l'angle avant le drag
                self.initial_position = self.position  # Sauvegarde de la position avant le drag
                self.velocity = pygame.math.Vector2(0, 0)  # Réinitialisation de la vitesse pendant le drag
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                # Calcul de l'angle de direction pour la rotation
                mouse_pos = pygame.math.Vector2(event.pos)
                direction_vector = mouse_pos - self.position
                
                # Calcul de l'angle avec atan2 pour une orientation correcte
                self.angle = -math.degrees(math.atan2(direction_vector.y, direction_vector.x)) + 90

                # Appliquer la rotation
                self.image = pygame.transform.rotate(self.original_image, self.angle)
                
                # Ajuster la position du rectangle pour que le centre ne change pas
                self.rect = self.image.get_rect(center=self.rect.center)
                
                # Calcul de la vitesse pour le lancement
                drag_distance = direction_vector.length()
                self.velocity = -direction_vector.normalize() * drag_distance * 0.001  # Multiplier pour ajuster la vitesse



        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                self.has_launched = True  # Interdit tout autre lancement
                self.launch_velocity = self.velocity  # Sauvegarde la vitesse de lancement du vaisseau

        
    def explode(self):
        """Gère l'explosion du vaisseau"""
        self.exploded = True  # Le vaisseau est maintenant explosé
        self.image = self.explosion_image  # Changement de l'image pour celle de l'explosion
        self.rect = self.image.get_rect(center=self.rect.center)  # Ajuste la position du rectangle avec l'image d'explosion
    
    def move(self):
        """Déplace le vaisseau pendant le jeu"""
        if not self.dragging:  # Si le vaisseau n'est pas en train de glisser
            if self.fuel > 0:
                # Mise à jour de la position du vaisseau en fonction de la vitesse
                self.position += self.velocity
                self.rect.center = (int(self.position.x), int(self.position.y))  # Mise à jour du rectangle pour suivre la position

    def draw_fuel_bar(self, screen):
        """Dessine la barre de carburant en haut de l'écran avec le texte 'Carburant'."""
        fuel_width = 1000  # Largeur de la barre de carburant
        fuel_height = 60  # Hauteur de la barre de carburant
        fuel_percentage = self.fuel / self.fuel_max  # Pourcentage du carburant restant

        # Récupère la largeur de l'écran
        screen_width = screen.get_width()

        # Dessiner l'arrière-plan de la barre de carburant
        pygame.draw.rect(screen, (50, 50, 50), (screen_width // 2 - fuel_width // 2, 40, fuel_width, fuel_height))

        # Dessiner la barre de carburant
        pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - fuel_width // 2, 40, int(fuel_width * fuel_percentage), fuel_height))

        # Dessiner le texte "Carburant"
        font = pygame.font.SysFont("Arial", 40)  # Police pour le texte
        text_surface = font.render("Carburant", True, (255, 0, 0))  # Créer le texte
        text_rect = text_surface.get_rect(center=(screen_width // 2, 70))  # Centrer le texte
        screen.blit(text_surface, text_rect)  # Afficher le texte sur l'écran