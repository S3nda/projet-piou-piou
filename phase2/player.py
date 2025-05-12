import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, position, fuel, image_path, explosion_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=position)
        
        self.position = pygame.math.Vector2(position)
        
        self.velocity = pygame.math.Vector2(0, 0)
        
        self.fuel = fuel
        self.fuel_max = fuel
        
        self.explosion_image = pygame.image.load(explosion_path).convert_alpha()
        self.exploded = False
        
        self.angle = 0
        
        self.dragging = False
        
        self.fuel_consume_rate = 0.01
        self.fuel_drain_factor = 0.1

        self.gravity_strength = 0.1
        self.gravity_range = 200

        self.has_launched = False


    def update(self, dt, planets):
        """Met à jour la position et l'état du vaisseau"""
        if self.fuel > 0 and not self.dragging:
            self.position += self.velocity * dt
            self.rect.center = (int(self.position.x), int(self.position.y))
            self.fuel -= self.velocity.length() * self.fuel_drain_factor * dt
            self.fuel = max(self.fuel, 0)

        # Applique la gravité des planètes
        self.apply_gravity(planets)

        # Applique la rotation en fonction de l'angle
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def apply_gravity(self, planets):
        """Applique la gravité des planètes sur le vaisseau."""
        total_gravity_force = pygame.math.Vector2(0, 0)

        for planet in planets:
            dx = planet.position.x - self.position.x
            dy = planet.position.y - self.position.y
            distance = math.sqrt(dx**2 + dy**2)
            
            zone_attraction = (planet.rect.width / 2) * 3
            
            if distance < zone_attraction:
                force_magnitude = 100 / (distance ** 1.5)

                force_reduction_factor = 0.2
                force_magnitude *= force_reduction_factor 
                
                force_direction = pygame.math.Vector2(dx, dy).normalize()

                gravity_force = force_direction * force_magnitude
                
                total_gravity_force += gravity_force
    
        self.velocity += total_gravity_force

    def handle_event(self, event):
        """Gère les événements du jeu (clavier, souris, etc.)"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.has_launched:
                self.dragging = True
                self.drag_start_pos = pygame.math.Vector2(event.pos)
                self.initial_angle = self.angle
                self.initial_position = self.position
                self.velocity = pygame.math.Vector2(0, 0)
                
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_pos = pygame.math.Vector2(event.pos)
                direction_vector = mouse_pos - self.position
                
                self.angle = -math.degrees(math.atan2(direction_vector.y, direction_vector.x)) + 90

                self.image = pygame.transform.rotate(self.original_image, self.angle)
                
                self.rect = self.image.get_rect(center=self.rect.center)
                
                drag_distance = direction_vector.length()
                self.velocity = -direction_vector.normalize() * drag_distance * 0.001

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:
                self.dragging = False
                self.has_launched = True
                self.launch_velocity = self.velocity
        
    def explode(self):
        """Gère l'explosion du vaisseau"""
        self.exploded = True
        self.image = self.explosion_image
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def move(self):
        """Déplace le vaisseau pendant le jeu"""
        if not self.dragging:
            if self.fuel > 0:
                self.position += self.velocity
                self.rect.center = (int(self.position.x), int(self.position.y))

    def draw_fuel_bar(self, screen):
        """Dessine la barre de carburant en haut de l'écran avec le texte 'Carburant'."""
        fuel_width = 1000
        fuel_height = 60
        fuel_percentage = self.fuel / self.fuel_max

        screen_width = screen.get_width()

        pygame.draw.rect(screen, (50, 50, 50), (screen_width // 2 - fuel_width // 2, 40, fuel_width, fuel_height))

        pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - fuel_width // 2, 40, int(fuel_width * fuel_percentage), fuel_height))

        font = pygame.font.SysFont("Arial", 40)
        text_surface = font.render("Carburant", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(screen_width // 2, 70))
        screen.blit(text_surface, text_rect)
