import pygame
import math
from bullet import Bullet

class Player:
    def __init__(self, x, y):
        self.pos = pygame.math.Vector2(x,y)
        self.speed = 4
        self.colour = (0,150,200)
        self.size = 20
        self.score = 1
        self.trail = []
        self.trail_length = 15
        self.angle = 0
        self.shoot_timer = 0
        self.shoot_delay = 30
        self.path_choice = None
        self.multishot = 1
        self.homing = False

        self.path_tiers = {"A": 0, "B": 0}

        self.sprite_forward = pygame.image.load("sprites/ShooterMcGee_forward.png")
        self.sprite_backward = pygame.image.load("sprites/ShooterMcGee_backward.png")
        self.sprite_move = pygame.image.load("sprites/ShooterMcGee_shrink.png")
        self.sprite_move_backwards = pygame.image.load("sprites/ShooterMcGee_shrink_backwards.png")

        self.current_side_sprite = self.sprite_forward
        self.moving = False
        self.sprite_swap_timer = 0
        self.sprite_swap_rate = 12
        self.show_move_sprite = False

    def shoot(self, bullets, mouse_x, mouse_y):
        base_angle = math.atan2(mouse_y - self.pos.y, mouse_x - self.pos.x)
        spread = 15
        for i in range(self.multishot):
            offset = (i - (self.multishot -1) / 2) * spread
            rad = base_angle + math.radians(offset)
            tx = self.pos.x + math.cos(rad) * 200
            ty = self.pos.y + math.sin(rad) * 200
            bullets.append(Bullet(self.pos.x, self.pos.y, tx, ty, homing=self.homing))

    def update(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0,0)

        self.shoot_timer += 1

        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
            self.current_side_sprite = self.sprite_backward
        if keys[pygame.K_d]:
            direction.x += 1
            self.current_side_sprite = self.sprite_forward

        #Normalize
        self.moving = False
        if direction.length() > 0:
            direction = direction.normalize()
            self.moving = True

        if self.moving:
            self.sprite_swap_timer += 1
            if self.sprite_swap_timer >= self.sprite_swap_rate:
                self.sprite_swap_timer = 0
                self.show_move_sprite = not self.show_move_sprite

        else:
            self.sprite_swap_timer = 0
            self.show_move_sprite = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.angle = math.atan2(mouse_y - self.pos.y, mouse_x - self.pos.x)
        self.pos += direction * self.speed

        if self.moving:
            self.trail.append((self.pos.copy(), self.angle, self.get_current_sprite()))
        else:
            if self.trail:
                self.trail.pop(0)

        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def get_current_sprite(self):
        if self.current_side_sprite== self.sprite_forward:
            return self.sprite_move if self.show_move_sprite else self.sprite_forward
        elif self.current_side_sprite == self.sprite_backward:
            return self.sprite_move_backwards if self.show_move_sprite else self.sprite_backward 
        return self.current_side_sprite

        
    def draw(self, screen, offset_x=0, offset_y=0):
        for i, (pos, angle, sprite) in enumerate(self.trail):
            alpha = int(180 * (i / max(self.trail_length, 1)))

            trail_surface = pygame.Surface((self.size*3, self.size*3), pygame.SRCALPHA)
            trail_surface.blit(sprite, (0,0))
            trail_surface.set_alpha(alpha)
            rect = trail_surface.get_rect(center=(int(pos.x + offset_x), int(pos.y + offset_y)))
            screen.blit(trail_surface, rect)
        
        sprite = self.get_current_sprite()
        if sprite is None:
            sprite = self.current_side_sprite

        sprite_rect = sprite.get_rect(center=(int(self.pos.x + offset_x), int(self.pos.y + offset_y)))
        screen.blit(sprite, sprite_rect)

