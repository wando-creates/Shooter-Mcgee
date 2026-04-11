
import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.pos = pygame.math.Vector2(x,y)

        direction = pygame.math.Vector2(target_x - x, target_y - y)

        if direction.length() > 0:
            direction = direction.normalize()

        self.speed = 10
        self.velocity = direction * self.speed

        self.radius = 2
        self.colour = (255,200,0)

    def update(self):
        self.pos += self.velocity
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (int(self.pos.x), int(self.pos.y)), self.radius)

    def hit_wall(self, width, height):
        return (self.pos.x <= 0 or self.pos.x >= width or
                self.pos.y <= 0 or self.pos.y >= height)