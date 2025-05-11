import pygame
import random
import os
from player import Player
from planet import Planet
from target import Target

# Constantes
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
FPS = 60  # Frames par seconde (pour la gestion du temps)

# Couleurs
WHITE = (255, 255, 255)

# Fonction principale du jeu
def main_phase2():
    # Initialisation de Pygame
    pygame.init()
    
    # Création de l'écran
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Void Seekers - Phase 2")
    
    # Horloge pour la gestion du temps (delta time)
    clock = pygame.time.Clock()
    
    # Choix aléatoire du fond
    background_folder = "../assets/background/"
    background_images = [f for f in os.listdir(background_folder) if f.endswith(".png")]
    if not background_images:
        raise FileNotFoundError(f"Aucune image trouvée dans le dossier {background_folder}")
    
    chosen_background = random.choice(background_images)
    background = pygame.image.load(os.path.join(background_folder, chosen_background)).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Création du joueur
    player = Player(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), fuel=100, image_path="../assets/player.png", explosion_path="../assets/explosion.png")
    
    # Création de la planète cible
    target_planet = Target(position=(random.randint(200, 600), random.randint(100, 500)), mass=0.5, gravity_range=60, image_path="../assets/target.png")
    
    # Fonction pour vérifier si une planète est trop proche d'une autre
    def is_planet_too_close(new_planet_pos, planets, target_planet):
        for planet in planets:
            distance_to_planet = pygame.math.Vector2(new_planet_pos).distance_to(planet.position)
            if distance_to_planet < (planet.rect.width / 2 + 50):  # Si la distance est trop petite
                return True
        distance_to_target = pygame.math.Vector2(new_planet_pos).distance_to(target_planet.position)
        if distance_to_target < (target_planet.rect.width / 2 + 50):  # Vérifie si elle est trop proche de la cible
            return True
        return False

    # Création des planètes obstacles (aléatoires) avec une vérification de la distance entre elles et de la cible
    planets = []
    for _ in range(3):
        while True:
            # Génération de la position de la planète aléatoirement
            planet_pos = (random.randint(200, 600), random.randint(100, 500))
            
            # Génération de la masse (entre 1 et 3) et du champ gravitationnel (utilisé pour la zone de gravité)
            mass = random.randint(1, 3)
            gravity_range = random.randint(200, 300)  # Plage de la gravité

            # Choix aléatoire de la taille de la planète parmi 3 valeurs fixes (80, 100, 120)
            size_choices = [80, 100, 120]
            planet_size = random.choice(size_choices)  # Choisit aléatoirement une taille parmi les 3 options

            # Vérification des distances avec les autres planètes et la cible
            if not is_planet_too_close(planet_pos, planets, target_planet):
                # Créer la planète avec la taille choisie
                planets.append(Planet(position=planet_pos, mass=mass, gravity_range=gravity_range, size=planet_size))
                break  # Sortir de la boucle lorsque la position est correcte


    # Groupe de sprites pour faciliter la gestion des objets
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(target_planet)
    for planet in planets:
        all_sprites.add(planet)

    # Variables de jeu
    running = True
    last_time = pygame.time.get_ticks()
    dt = 0  # Temps écoulé depuis la dernière mise à jour (en millisecondes)

    while running:
        # Calcul du delta time (temps écoulé entre deux frames)
        dt = pygame.time.get_ticks() - last_time
        last_time = pygame.time.get_ticks()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_event(event)

        # Mise à jour de l'état du jeu
        player.update(dt, planets)  # Mise à jour de la position du joueur et prise en compte des planètes
        for planet in planets:
            planet.update(dt)  # Mise à jour de chaque planète (si nécessaire)
        
        # Vérification des collisions entre le joueur et la cible
        distance_to_target = player.position.distance_to(target_planet.position)
        if distance_to_target < (player.rect.width / 2 + target_planet.rect.width / 2):
            print("Victoire ! Vous avez atteint la cible.")
            running = False

        # Vérification des collisions avec les planètes obstacles
        for planet in planets:
            distance_to_planet = player.position.distance_to(planet.position)
            if distance_to_planet < (player.rect.width / 2 + planet.rect.width / 2):
                player.explode()
                print("Perdu ! Vous avez percuté une planète obstacle.")
                running = False

        # Affichage du fond
        screen.blit(background, (0, 0))

        # Affichage des objets
        all_sprites.draw(screen)

        # Affichage de la barre de carburant
        player.draw_fuel_bar(screen)

        # Mise à jour de l'écran
        pygame.display.flip()
        
        # Limitation du nombre de frames par seconde
        clock.tick(FPS)

    # Quitter Pygame proprement
    pygame.quit()

# Appeler la fonction principale si ce fichier est exécuté
if __name__ == "__main__":
    main_phase2()