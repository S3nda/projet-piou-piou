import pygame
import random
import os
from player import Player
from planet import Planet
from target import Target

# Constantes
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Définir l'écran en mode plein écran
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()  # Récupérer les dimensions de l'écran
FPS = 60  # Frames par seconde (pour la gestion du temps)

# Couleurs
WHITE = (255, 255, 255)  # Définir la couleur blanche

# Fonction principale du jeu
def main_phase2():
    # Initialisation de Pygame
    pygame.init()
    
    # Création de l'écran
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Créer la fenêtre du jeu avec les dimensions
    pygame.display.set_caption("Void Seekers - Phase 2")  # Définir le titre de la fenêtre
    
    # Horloge pour la gestion du temps (delta time)
    clock = pygame.time.Clock()  # Créer une horloge pour gérer les FPS
    
    # Choix aléatoire du fond
    background_folder = "../assets/background/"  # Dossier des images de fond
    background_images = [f for f in os.listdir(background_folder) if f.endswith(".png")]  # Liste des images .png
    if not background_images:
        raise FileNotFoundError(f"Aucune image trouvée dans le dossier {background_folder}")  # Vérifier si le dossier contient des images
    
    chosen_background = random.choice(background_images)  # Choisir une image de fond aléatoire
    background = pygame.image.load(os.path.join(background_folder, chosen_background)).convert()  # Charger l'image
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Adapter l'image à la taille de l'écran

    # Création du joueur
    player = Player(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), fuel=100, image_path="../assets/player.png", explosion_path="../assets/explosion.png")
    
    # Création de la planète cible
    target_planet = Target(position=(random.randint(200, 600), random.randint(100, 500)), mass=0.5, gravity_range=60, image_path="../assets/target.png")
    
    # Fonction pour vérifier si une planète est trop proche d'une autre
    def is_planet_too_close(new_planet_pos, planets, target_planet):
        # Vérification des distances avec les autres planètes
        for planet in planets:
            distance_to_planet = pygame.math.Vector2(new_planet_pos).distance_to(planet.position)
            if distance_to_planet < (planet.rect.width / 2 + 100):  # Si la distance est trop petite entre obstacles
                return True
        # Vérification de la distance avec la planète cible
        distance_to_target = pygame.math.Vector2(new_planet_pos).distance_to(target_planet.position)
        if distance_to_target < (target_planet.rect.width / 2 + 100):  # Vérifie si elle est trop proche de la cible
            return True
        return False  # Si aucune planète n'est trop proche, retourne False

    # Création des planètes obstacles (aléatoires) avec une vérification de la distance entre elles et de la cible
    planets = []  # Liste pour stocker les planètes obstacles
    for _ in range(3):  # Créer 3 planètes obstacles
        while True:
            # Génération de la position de la planète aléatoirement, plus loin de la planète cible et des autres obstacles
            planet_pos = (random.randint(200, 800), random.randint(100, 600))
            
            # Génération de la masse (entre 1 et 3) et du champ gravitationnel (utilisé pour la zone de gravité)
            mass = random.randint(1, 3)
            gravity_range = random.randint(200, 300)  # Plage de la gravité

            # Choix aléatoire de la taille de la planète parmi 3 valeurs fixes (80, 100, 120)
            size_choices = [80, 100, 120]
            planet_size = random.choice(size_choices)  # Choisit aléatoirement une taille parmi les 3 options

            # Vérification des distances avec les autres planètes et la cible
            if not is_planet_too_close(planet_pos, planets, target_planet):
                # Créer la planète avec la taille choisie si la distance est correcte
                planets.append(Planet(position=planet_pos, mass=mass, gravity_range=gravity_range, size=planet_size))
                break  # Sortir de la boucle lorsque la position est correcte

    # Groupe de sprites pour faciliter la gestion des objets
    all_sprites = pygame.sprite.Group()  # Créer un groupe de sprites
    all_sprites.add(player)  # Ajouter le joueur au groupe
    all_sprites.add(target_planet)  # Ajouter la planète cible au groupe
    for planet in planets:  # Ajouter toutes les planètes obstacles au groupe
        all_sprites.add(planet)

    # Variables de jeu
    running = True  # Variable pour contrôler l'état du jeu
    last_time = pygame.time.get_ticks()  # Dernier temps enregistré pour le calcul du delta time
    dt = 0  # Temps écoulé depuis la dernière mise à jour (en millisecondes)

    while running:
        # Calcul du delta time (temps écoulé entre deux frames)
        dt = pygame.time.get_ticks() - last_time
        last_time = pygame.time.get_ticks()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si l'utilisateur ferme la fenêtre
                running = False
            player.handle_event(event)  # Gérer les événements liés au joueur

        # Mise à jour de l'état du jeu
        player.update(dt, planets)  # Mise à jour de la position du joueur et prise en compte des planètes
        for planet in planets:  # Mise à jour de chaque planète (si nécessaire)
            planet.update(dt)
        
        # Vérification des collisions entre le joueur et la cible
        distance_to_target = player.position.distance_to(target_planet.position)
        if distance_to_target < (player.rect.width / 2 + target_planet.rect.width / 2):
            print("Victoire ! Vous avez atteint la cible.")  # Message de victoire
            running = False

        # Vérification des collisions avec les planètes obstacles
        for planet in planets:
            distance_to_planet = player.position.distance_to(planet.position)
            if distance_to_planet < (player.rect.width / 2 + planet.rect.width / 2):
                player.explode()  # Le joueur explose en cas de collision avec une planète obstacle
                print("Perdu ! Vous avez percuté une planète obstacle.")  # Message de défaite
                running = False

        # Affichage du fond
        screen.blit(background, (0, 0))  # Afficher le fond à l'écran

        # Affichage des objets
        all_sprites.draw(screen)  # Dessiner tous les objets du groupe de sprites

        # Affichage de la barre de carburant
        player.draw_fuel_bar(screen)  # Afficher la barre de carburant du joueur

        # Mise à jour de l'écran
        pygame.display.flip()  # Rafraîchir l'écran
        
        # Limitation du nombre de frames par seconde
        clock.tick(FPS)  # Limiter la boucle de jeu à 60 FPS

    # Quitter Pygame proprement
    pygame.quit()

# Appeler la fonction principale si ce fichier est exécuté
if __name__ == "__main__":
    main_phase2()  # Démarrer la phase 2 du jeu