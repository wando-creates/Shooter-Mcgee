import pygame
import math

class Player:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x,y)
        self.speed = 4
        self.colour = (0,150,200)
        self.size = 20

        self.trail = []
        self.trail_length = 15

        self.angle = 0

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
        moving = False
        if direction.length() > 0:
            direction = direction.normalize()
            moving = True

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.pos.y, mouse_x - self.pos.x)

        self.pos += direction * self.speed
        if moving:
            self.trail.append((self.pos.copy(), self.angle))
        else:
            if self.trail:
                self.trail.pop(0)
                
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw(self, screen, offset_x=0, offset_y=0):
        for i, (pos, angle) in enumerate(self.trail):
            alpha = int(255 * (i / self.trail_length))

            trail_surface = pygame.Surface((self.size*6, self.size*6), pygame.SRCALPHA)
            center = self.size * 1.5

            tip = (center + math.cos(angle) * self.size + offset_x,
                center + math.sin(angle) * self.size + offset_y)
            left = (center + math.cos(angle + 2.5) * self.size + offset_x,
                    center + math.sin(angle + 2.5) * self.size + offset_y)
            right = (center + math.cos(angle - 2.5) * self.size + offset_x,
                    center + math.sin(angle - 2.5) * self.size + offset_y)
            
            pygame.draw.polygon(trail_surface, (*self.colour, alpha), [tip, left, right])
            screen.blit(trail_surface, (pos.x - center + offset_x, pos.y - center + offset_y))
        
        angle = self.angle

        tip = (self.pos.x + math.cos(angle) * self.size + offset_x,
            self.pos.y + math.sin(angle) * self.size + offset_y)
        left = (self.pos.x + math.cos(angle + 2.5) * self.size + offset_x,
                self.pos.y + math.sin(angle + 2.5) * self.size + offset_y)
        right = (self.pos.x + math.cos(angle - 2.5) * self.size + offset_x,
                self.pos.y + math.sin(angle - 2.5) * self.size + offset_y)

        pygame.draw.polygon(screen, self.colour, [tip, left, right])

