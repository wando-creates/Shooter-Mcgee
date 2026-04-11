import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = (0,150,200)
        self.size = 20

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

        tip = (self.x + math.cos(angle) * self.size,
               self.y + math.sin(angle) * self.size)
        left = (self.x + math.cos(angle + 2.5) * self.size,
                self.y + math.sin(angle + 2.5) * self.size)
        right = (self.x + math.cos(angle - 2.5) * self.size,
                 self.y + math.sin(angle - 2.5) * self.size)
        

        pygame.draw.polygon(screen, self.colour, [tip, left, right])
