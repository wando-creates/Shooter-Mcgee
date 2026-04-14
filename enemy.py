import pygame
import math
import random

BLOON_TYPES = {
    "red": {"speed": 1.0, "health":1, "colour": (120,20,20)},
    "blue": {"speed": 1.15, "health":2, "colour": (0,50,120)},
    "green": {"speed": 1.3, "health":3, "colour": (0,120,50)},
    "yellow": {"speed": 1.6, "health":4, "colour": (120,120,0)},
    "pink": {"speed": 1.7, "health":5, "colour": (120,52,90)}
}

class Enemy:
    def __init__(self, x, y, bloon_type="red"):
        self.pos = pygame.math.Vector2(x, y)
        self.type = bloon_type

        data = BLOON_TYPES[bloon_type]
        self.speed = data["speed"]
        self.health = data["health"]
        self.colour = data["colour"]

        self.radius = 15

    def update(self, player_pos):
        direction = player_pos - self.pos

        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed
    
    def draw(self, screen, offset_x=0, offset_y=0):
        pygame.draw.circle(screen, self.colour, (int(self.pos.x + offset_x), int(self.pos.y + offset_y)), self.radius)
        