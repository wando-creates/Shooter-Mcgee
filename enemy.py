import pygame
import math
import random

class Enemy:
    def __init__(self, x, y, health=2):
        self.pos = pygame.math.Vector2(x, y)
        self.speed = 1
        self.radius = 15
        self.health = health

    def update(self, player_pos):
        direction = player_pos - self.pos

        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed
    
    def draw(self, screen, offset_x=0, offset_y=0):
        if self.health == 3:
            colour = (0, 255, 100)
        elif self.health == 2:
            colour = (0,100,255)
        elif self.health == 1:
            colour = (255, 50, 50)
        elif self.health <= 0:
            return
        
        pygame.draw.circle(screen, colour, (int(self.pos.x + offset_x), int(self.pos.y + offset_y)), self.radius)
