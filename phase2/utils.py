import pygame
import random
import math

def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def normalize(v):
    length = math.hypot(v[0], v[1])
    if length == 0:
        return (0, 0)
    return (v[0] / length, v[1] / length)

def random_position(rect, margin=0):
    x = random.randint(rect.left + margin, rect.right - margin)
    y = random.randint(rect.top + margin, rect.bottom - margin)
    return (x, y)