import pygame
import math

def distance(point1, point2):
    """Calcule la distance entre deux points."""
    return point1.distance_to(point2)

def normalize(vector):
    """Normalise un vecteur pour qu'il ait une magnitude de 1."""
    if vector.length() == 0:
        return pygame.math.Vector2(0, 0)
    return vector.normalize()

def gravitational_force(mass1, mass2, pos1, pos2):
    """Retourne la force gravitationnelle entre deux objets selon la loi de la gravitation de Newton."""
    G = 6.67430e-11  # Constante gravitationnelle (en m^3 kg^-1 s^-2)
    distance = pos1.distance_to(pos2)  # Distance entre les deux objets
    
    if distance == 0:  # Éviter la division par zéro si les objets sont au même endroit
        return pygame.math.Vector2(0, 0)

    force_magnitude = (G * mass1 * mass2) / (distance ** 2)  # Loi de la gravité de Newton
    force_direction = (pos2 - pos1).normalize()  # Direction de la force, du joueur vers la planète
    
    return force_direction * force_magnitude  # Retourne la force sous forme de vecteur

def add_vectors(v1, v2):
    """Additionne deux vecteurs."""
    return v1 + v2

def multiply_vector(vector, scalar):
    """Multiplie un vecteur par un scalaire."""
    return vector * scalar