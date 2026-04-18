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

blue_boss = pygame.image.load("sprites/blue_boss.png")
blue_boss_2 = pygame.image.load("sprites/blue_boss_2.png")

blue_boss_left = pygame.image.load("sprites/blue_boss_left.png")
blue_boss_2_left = pygame.image.load("sprites/blue_boss_2_left.png")

BLOON_TYPES = {
    "red": {"speed": 1.5, "health":1, "frames": [red, red_2], "colour": (255,60,60)},
    "blue": {"speed": 1.65, "health":2, "frames": [blue, blue_2], "colour": (60,60,255)},
    "green": {"speed": 1.7, "health":3, "frames": [green, green_2], "colour": (60,255,60)},
    "yellow": {"speed": 2.3, "health":4, "frames": [yellow, yellow_2], "colour": (255,255,60)},
    "pink": {"speed": 2.8, "health":5, "frames": [pink, pink_2], "colour": (255,100,200)},
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
        self.menu_direction = 0

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

    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    def draw(self, screen, offset_x=0, offset_y=0):

 
        image = self.frames[self.frame_index]

        rect = image.get_rect(center=(int(self.pos.x + offset_x), int(self.pos.y + offset_y)))
        screen.blit(image, rect)

class Boss:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x,y)
        self.type = "blue_boss"
        self.speed = 2
        self.health = 50
        self.max_health = 50
        self.colour = (1,74,96)
        self.radius = 50
        
        self.frames_right = [blue_boss, blue_boss_2]
        self.frames_left = [blue_boss_left, blue_boss_2_left]

        self.frame_index = 0
        self.animation_timer = 0 
        self.animation_speed = 10
        self.facing_right = True

    def update(self, player_pos):
        direction = player_pos - self.pos

        self.facing_right = player_pos.x >= self.pos.x

        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            frame_count = len(self.frames_right)
            self.frame_index = (self.frame_index + 1) % frame_count
        
        if direction.length() > 0:
            direction = direction.normalize()
            self.pos += direction * self.speed
    
    def draw(self, screen, offset_x=0, offset_y=0):
        frames = self.frames_right if self.facing_right else self.frames_left
        image = frames[self.frame_index]
        rect = image.get_rect(center=(int(self.pos.x + offset_x), int(self.pos.y + offset_y)))
        screen.blit(image, rect)

        bar_width = 120
        bar_height = 10
        bar_x = int(self.pos.x + offset_x) - bar_width // 2
        bar_y = int(self.pos.y + offset_y) - self.radius - 20

        pygame.draw.rect(screen, (60,0,0), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        fill = int(bar_width * (self.health / self.max_health))
        if fill > 0:
            pygame.draw.rect(screen, (220,40,40), (bar_x, bar_y, fill, bar_height), border_radius=4)
        pygame.draw.rect(screen, (20,20,20), (bar_x, bar_y, bar_width, bar_height), 1, border_radius=4)
