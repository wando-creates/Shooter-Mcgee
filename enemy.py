import pygame
import math
import random

BLOON_TYPES = {
    "red": {"speed": 1.0, "health":1, "colour": (255,50,50)},
    "blue": {"speed": 1.15, "health":2, "colour": (0,100,255)},
    "green": {"speed": 1.3, "health":3, "colour": (0,255,100)},
    "yellow": {"speed": 1.6, "health":4, "colour": (255,255,0)},
    "pink": {"speed": 1.7, "health":5, "colour": (255,105,180)}
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
        