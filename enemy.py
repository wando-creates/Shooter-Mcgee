import pygame
import math
import random

red = pygame.image.load("sprites/Red.png")
red_2 = pygame.image.load("sprites/Red_2.png")

blue = pygame.image.load("sprites/Blue.png")
blue_2 = pygame.image.load("sprites/Blue_2.png")

green = pygame.image.load("sprites/Green.png")
green_2 = pygame.image.load("sprites/Green_2.png")

yellow = pygame.image.load("sprites/Yellow.png")
yellow_2 = pygame.image.load("sprites/Yellow_2.png")

pink = pygame.image.load("sprites/Pink.png")
pink_2 = pygame.image.load("sprites/Pink_2.png")

BLOON_TYPES = {
    "red": {"speed": 1.0, "health":1, "frames": [red, red_2], "colour": (255,60,60)},
    "blue": {"speed": 1.15, "health":2, "frames": [blue, blue_2], "colour": (60,60,255)},
    "green": {"speed": 1.3, "health":3, "frames": [green, green_2], "colour": (60,255,60)},
    "yellow": {"speed": 2, "health":4, "frames": [yellow, yellow_2], "colour": (255,255,60)},
    "pink": {"speed": 2.5, "health":5, "frames": [pink, pink_2], "colour": (255,100,200)}
}


class Enemy:
    def __init__(self, x, y, bloon_type="red"):
        self.pos = pygame.math.Vector2(x, y)
        self.type = bloon_type

        data = BLOON_TYPES[bloon_type]
        self.speed = data["speed"]
        self.health = data["health"]
        self.colour = data["colour"]
        self.radius = 25

        self.frames = data["frames"]
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 10


    def update(self, player_pos):
        direction = player_pos - self.pos
        self.animation_timer += 1
  
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed

    def draw(self, screen, offset_x=0, offset_y=0):

 
        image = self.frames[self.frame_index]

        rect = image.get_rect(center=(int(self.pos.x + offset_x), int(self.pos.y + offset_y)))
        screen.blit(image, rect)
