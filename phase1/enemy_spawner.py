import pygame
from phase1.enemy import Enemy
import math
import random


class EnemySpawner:
    def __init__(self, screen):
        self.screen = screen
        self.enemies = pygame.sprite.Group()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.wave_patterns = {
            # Définition des différentes vagues
            1: self._wave_basic_line,
            2: self._wave_v_formation,
            3: self._wave_circle_formation,
            4: self._wave_zigzag,
            5: self._wave_crossfire,
            6: self._wave_boss_with_minions,
            7: self._wave_random_swarm,
            8: self._wave_pincer_movement,
            9: self._wave_spiral_attack,
            10: self._wave_final_assault,
            11: self._test_wave,
        }

    def spawn_wave(self, wave_id):
        """Lance une vague d'ennemis selon l'ID spécifié"""
        if wave_id in self.wave_patterns:
            wave_function = self.wave_patterns[wave_id]
            return wave_function()
        else:
            print(f"Vague {wave_id} non définie!")
            return []

    def update(self, dt):
        """Met à jour tous les ennemis"""
        for enemy in self.enemies:
            enemy.update(dt)

            # Supprimer les ennemis qui sortent complètement de l'écran
            if (
                enemy.pos.y > self.screen_height + 200
                or enemy.pos.y < -200
                or enemy.pos.x < -200
                or enemy.pos.x > self.screen_width + 200
            ):
                self.enemies.remove(enemy)

    def draw(self, surface):
        """Dessine tous les ennemis"""
        for enemy in self.enemies:
            enemy.draw(surface)

    def _test_wave(self):
        enemy = Enemy(self.screen_width // 2, self.screen_height // 2, self.screen)
        self.enemies.add(enemy)
        return

    def _wave_basic_line(self):
        enemies_created = []
        spacing = 200
        num_enemies = 5

        for i in range(num_enemies):
            x = (
                self.screen_width // 2
                - ((num_enemies - 1) * spacing) // 2
                + i * spacing
            )
            y = 0
            enemy = Enemy(x, y, self.screen)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_v_formation(self):
        """Vague 2: Formation en V qui descend"""
        enemies_created = []
        num_enemies = 5

        # Position centrale en haut de l'écran
        center_x = self.screen_width // 2
        start_y = 100

        # Créer une formation en V
        for i in range(num_enemies):
            # Position x décalée par rapport au centre
            offset = 100 * i

            # Ennemi à gauche
            left_x = center_x - offset
            left_enemy = Enemy(
                left_x,
                start_y,
                self.screen,
                instructions=[
                    (0, -300, 10),  # Descendre de 300px, attendre 1s
                    (100 * i, 100, 0.5),  # Se déplacer en diagonale, attendre 0.5s
                    (-100, 0, 0.5),  # Aller à gauche, attendre 0.5s
                    (0, 200, 0),  # Continuer à descendre
                ],
            )
            self.enemies.add(left_enemy)
            enemies_created.append(left_enemy)

            # Ennemi à droite (sauf au centre pour éviter la duplication)
            if i > 0:
                right_x = center_x + offset
                right_enemy = Enemy(
                    right_x,
                    start_y,
                    self.screen,
                    instructions=[
                        (0, 300, 1),  # Descendre de 300px, attendre 1s
                        (-100 * i, 100, 0.5),  # Se déplacer en diagonale, attendre 0.5s
                        (100, 0, 0.5),  # Aller à droite, attendre 0.5s
                        (0, 200, 0),  # Continuer à descendre
                    ],
                )
                self.enemies.add(right_enemy)
                enemies_created.append(right_enemy)

        return enemies_created

    def _wave_circle_formation(self):
        """Vague 3: Formation en cercle qui tourne"""
        enemies_created = []
        num_enemies = 8
        radius = 200
        center_x = self.screen_width // 2
        center_y = 300

        for i in range(num_enemies):
            # Calculer la position sur le cercle
            angle = (i / num_enemies) * 2 * 3.14159  # en radians
            x = (
                center_x
                + radius * pygame.math.Vector2(math.cos(angle), math.sin(angle)).x
            )
            y = (
                center_y
                + radius * pygame.math.Vector2(math.cos(angle), math.sin(angle)).y
            )

            # Créer des instructions pour faire tourner en cercle
            instructions = []
            for j in range(8):  # 8 segments pour faire un cercle complet
                next_angle = angle + (j + 1) * 3.14159 / 4
                next_x = (
                    center_x
                    + radius
                    * pygame.math.Vector2(math.cos(next_angle), math.sin(next_angle)).x
                )
                next_y = (
                    center_y
                    + radius
                    * pygame.math.Vector2(math.cos(next_angle), math.sin(next_angle)).y
                )

                dx = next_x - x if j == 0 else next_x - prev_x
                dy = next_y - y if j == 0 else next_y - prev_y
                instructions.append(
                    (dx, -dy, 0.5)
                )  # Attendre 0.5s entre chaque segment

                prev_x, prev_y = next_x, next_y

            # Après le cercle, descendre
            instructions.append((0, 300, 0))

            enemy = Enemy(x, y, self.screen, instructions=instructions, fire_rate=1200)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_zigzag(self):
        """Vague 4: Mouvement en zigzag"""
        enemies_created = []
        num_enemies = 3
        start_positions = [
            (self.screen_width // 4, -100),
            (self.screen_width // 2, -150),
            (3 * self.screen_width // 4, -100),
        ]

        for i in range(num_enemies):
            x, y = start_positions[i]

            # Créer un chemin en zigzag
            instructions = []
            for j in range(5):  # 5 zigzags
                # Aller à droite puis à gauche
                if j % 2 == 0:
                    instructions.append((200, 100, 0.2))  # Diagonale droite-bas
                    instructions.append((-200, 100, 0.2))  # Diagonale gauche-bas
                else:
                    instructions.append((-200, 100, 0.2))  # Diagonale gauche-bas
                    instructions.append((200, 100, 0.2))  # Diagonale droite-bas

            enemy = Enemy(x, y, self.screen, instructions=instructions, fire_rate=600)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_crossfire(self):
        """Vague 5: Croisement d'ennemis"""
        enemies_created = []

        # Groupe 1: De gauche à droite
        for i in range(3):
            x = -100
            y = 100 + i * 150
            instructions = [
                (self.screen_width + 200, 0, 3),  # Traverser l'écran, attendre 3s
                (-100, 0, 0),  # Retourner à gauche (hors écran)
                (self.screen_width + 200, 0, 3),  # Traverser à nouveau
            ]
            enemy = Enemy(x, y, self.screen, instructions=instructions, fire_rate=500)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        # Groupe 2: De droite à gauche
        for i in range(3):
            x = self.screen_width + 100
            y = 175 + i * 150
            instructions = [
                (
                    -(self.screen_width + 200),
                    0,
                    3,
                ),  # Traverser l'écran dans l'autre sens
                (100, 0, 0),  # Retourner à droite (hors écran)
                (-(self.screen_width + 200), 0, 3),  # Traverser à nouveau
            ]
            enemy = Enemy(x, y, self.screen, instructions=instructions, fire_rate=500)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_boss_with_minions(self):
        """Vague 6: Boss au centre avec des petits ennemis qui tournent autour"""
        enemies_created = []

        # Boss au centre
        boss_x = self.screen_width // 2
        boss_y = 200

        # Le boss a plus de vie et un taux de tir plus élevé
        boss = Enemy(
            boss_x,
            boss_y,
            self.screen,
            health=10,
            fire_rate=300,
            instructions=[
                (200, 0, 1),  # Droite, pause
                (0, 100, 1),  # Bas, pause
                (-200, 0, 1),  # Gauche, pause
                (0, -100, 1),  # Haut, pause
            ],
        )
        self.enemies.add(boss)
        enemies_created.append(boss)

        # 4 minions qui tournent autour du boss
        radius = 150
        for i in range(4):
            angle = (i / 4) * 2 * 3.14159
            x = boss_x + radius * math.cos(angle)
            y = boss_y + radius * math.sin(angle)

            # Instructions pour tourner autour du boss
            instructions = []
            for j in range(8):
                next_angle = angle + (j + 1) * 3.14159 / 4
                next_x = boss_x + radius * math.cos(next_angle)
                next_y = boss_y + radius * math.sin(next_angle)

                dx = next_x - x if j == 0 else next_x - prev_x
                dy = next_y - y if j == 0 else next_y - prev_y
                instructions.append((dx, -dy, 0.5))

                prev_x, prev_y = next_x, next_y

            minion = Enemy(
                x, y, self.screen, instructions=instructions, health=2, fire_rate=1000
            )
            self.enemies.add(minion)
            enemies_created.append(minion)

        return enemies_created

    def _wave_random_swarm(self):
        """Vague 7: Nuée aléatoire d'ennemis"""
        enemies_created = []
        num_enemies = 12

        for i in range(num_enemies):
            # Position aléatoire en haut de l'écran
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(-300, -50)

            # Instructions de mouvement semi-aléatoires
            instructions = []
            current_x, current_y = x, y

            for j in range(5):
                # Nouvelle position cible
                target_x = random.randint(100, self.screen_width - 100)
                target_y = current_y + random.randint(100, 200)

                dx = target_x - current_x
                dy = target_y - current_y
                wait_time = random.uniform(0.3, 1.0)

                instructions.append((dx, -dy, wait_time))
                current_x, current_y = target_x, target_y

            enemy = Enemy(
                x,
                y,
                self.screen,
                instructions=instructions,
                fire_rate=random.randint(800, 1500),
            )
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_pincer_movement(self):
        """Vague 8: Mouvement en tenaille"""
        enemies_created = []

        # Groupe gauche
        left_start_x = -100

        for i in range(5):
            y = 100 + i * 80

            # Mouvement: entrer par la gauche, avancer, attendre, attaquer vers la droite
            instructions = [
                (300, 0, 1),  # Entrer dans l'écran
                (self.screen_width // 4, 0, 2),  # Avancer un peu
                (self.screen_width // 2, 200, 0),  # Attaquer en diagonale
            ]

            enemy = Enemy(left_start_x, y, self.screen, instructions=instructions)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        # Groupe droit
        right_start_x = self.screen_width + 100

        for i in range(5):
            y = 100 + i * 80

            # Mouvement: entrer par la droite, avancer, attendre, attaquer vers la gauche
            instructions = [
                (-300, 0, 1),  # Entrer dans l'écran
                (-(self.screen_width // 4), 0, 2),  # Avancer un peu
                (-(self.screen_width // 2), 200, 0),  # Attaquer en diagonale
            ]

            enemy = Enemy(right_start_x, y, self.screen, instructions=instructions)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_spiral_attack(self):
        """Vague 9: Attaque en spirale"""
        enemies_created = []
        num_enemies = 12
        center_x = self.screen_width // 2
        center_y = -100

        # Créer une spirale qui descend
        for i in range(num_enemies):
            # Paramètres de la spirale
            radius = 50 + i * 20
            angle = (i / 2) * 3.14159  # Demi-tour par ennemi

            x = center_x + radius * math.cos(angle)
            y = center_y

            # Instructions pour continuer la spirale
            instructions = []
            current_x, current_y = x, y

            for j in range(10):  # 10 segments de spirale
                next_angle = angle + (j + 1) * 3.14159 / 5  # 1/5 de tour
                next_radius = radius + j * 10  # La spirale s'agrandit

                next_x = center_x + next_radius * math.cos(next_angle)
                next_y = center_y + j * 50  # Descendre progressivement

                dx = next_x - current_x
                dy = next_y - current_y

                instructions.append(
                    (dx, -dy, 0.3)
                )  # Attendre 0.3s entre chaque segment
                current_x, current_y = next_x, next_y

            # Après la spirale, attaquer vers le bas
            instructions.append((0, 400, 0))

            enemy = Enemy(x, y, self.screen, instructions=instructions, fire_rate=800)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        return enemies_created

    def _wave_final_assault(self):
        """Vague 10: Assaut final avec différents types d'ennemis"""
        enemies_created = []

        # 1. Ligne d'ennemis en haut
        for i in range(6):
            x = 100 + i * 150
            y = -50
            instructions = [
                (0, 150, 1),
                (random.choice([-100, 100]), 100, 0.5),
                (0, 200, 0),
            ]
            enemy = Enemy(x, y, self.screen, instructions=instructions, health=2)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        # 2. Ennemis rapides qui traversent l'écran
        for i in range(4):
            x = -100
            y = 200 + i * 100
            speed_multiplier = 2.0  # Plus rapide

            instructions = [
                (self.screen_width + 200, 0, 0.5),
                (-self.screen_width - 200, 0, 0),
            ]

            enemy = Enemy(x, y, self.screen, instructions=instructions, fire_rate=400)
            self.enemies.add(enemy)
            enemies_created.append(enemy)

        # 3. Boss central
        boss_x = self.screen_width // 2
        boss_y = 150

        # Mouvements complexes pour le boss
        boss_instructions = []
        for i in range(3):
            boss_instructions.extend(
                [
                    (200, 0, 0.8),  # Droite
                    (0, 100, 0.8),  # Bas
                    (-200, 0, 0.8),  # Gauche
                    (0, -100, 0.8),  # Haut
                ]
            )

        boss = Enemy(
            boss_x,
            boss_y,
            self.screen,
            instructions=boss_instructions,
            health=15,
            fire_rate=200,
        )
        self.enemies.add(boss)
        enemies_created.append(boss)

        return enemies_created
