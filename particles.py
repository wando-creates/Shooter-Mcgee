import pygame
import random
import math

class Collision:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x,y)

        angle = random.uniform(0, 6.28)
        speed = random.uniform(2, 6)

        self.velocity = pygame.math.Vector2(math.cos(angle) * speed,
                                            math.sin(angle) * speed)
        
        self.radius = random.randint(1,2)
        self.life = 30
        self.colour = (0,0,0)
    
    def update(self):
        self.pos += self.velocity
        self.life -= 1
    
    def draw(self, screen, offset_x=0, offset_y=0):
        if self.life > 0:
            pygame.draw.circle(screen, self.colour, (int(self.pos.x + offset_x), int(self.pos.y + offset_y)), self.radius)

    def is_dead(self):
        return self.life <= 0