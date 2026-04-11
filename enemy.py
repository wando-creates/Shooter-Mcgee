import pygame
import math
import random

class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 1
        self.radius = 15
        self.colour = (200, 100, 50)

    def update(self, player_pos):
        direction = player_pos - self.pos

        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.pos.x), int(self.pos.y)), self.radius)
