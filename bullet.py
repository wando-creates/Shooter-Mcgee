
import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, homing=False):
        self.pos = pygame.math.Vector2(x,y)

        direction = pygame.math.Vector2(target_x - x, target_y - y)

        if direction.length() > 0:
            direction = direction.normalize()

        self.speed = 10
        self.velocity = direction * self.speed

        self.angle = math.atan2(direction.y, direction.x)
        self.homing = homing

    def update(self, enemies=None):
        if self.homing and enemies:
            nearest, best_d = None, float("inf")
            for e in enemies:
                d = (e.pos - self.pos).length()
                if d < best_d:
                    best_d, nearest = d, e
            
            if nearest and best_d < 500:
                desired = (nearest.pos - self.pos).normalize() * self.speed
                self.velocity += (desired - self.velocity) * 0.1

                if self.velocity.length() > self.speed:
                    self.velocity = self.velocity.normalize() * self.speed
                self.angle = math.atan2(self.velocity.y, self.velocity.x)

        self.pos += self.velocity
    
    def draw(self, screen, offset_x=0, offset_y=0):
        length = 12
        width = 4

        tip = (self.pos.x + math.cos(self.angle) * length + offset_x,
               self.pos.y + math.sin(self.angle) * length + offset_y)
        back = (self.pos.x - math.cos(self.angle) * length * 0.5 + offset_x,
                self.pos.y - math.sin(self.angle) * length * 0.5 + offset_y)
        left = (back[0] + math.cos(self.angle + math.pi/2) * width,
                back[1] + math.sin(self.angle + math.pi/2) * width)
        right = (back[0] + math.cos(self.angle - math.pi/2) * width,
                 back[1] + math.cos(self.angle - math.pi/2) * width)

        pygame.draw.polygon(screen, (0,0,0), [tip,left,right])
        pygame.draw.polygon(screen, (255,255,255), [tip,left,right], 1)

    def hit_wall(self, width, height):
        return (self.pos.x <= 0 or self.pos.x >= width or
                self.pos.y <= 0 or self.pos.y >= height)