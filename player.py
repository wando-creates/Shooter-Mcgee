import pygame
import math

class Player:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x,y)
        self.speed = 0.4
        self.colour = (0,150,200)
        self.size = 20

    def update(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0,0)

        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1

        #Normalize
        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.pos.y, mouse_x - self.pos.x)

        tip = (self.pos.x + math.cos(angle) * self.size,
               self.pos.y + math.sin(angle) * self.size)
        left = (self.pos.x + math.cos(angle + 2.5) * self.size,
                self.pos.y + math.sin(angle + 2.5) * self.size)
        right = (self.pos.x + math.cos(angle - 2.5) * self.size,
                 self.pos.y + math.sin(angle - 2.5) * self.size)
        

        pygame.draw.polygon(screen, self.colour, [tip, left, right])

