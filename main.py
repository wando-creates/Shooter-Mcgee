import pygame
import random
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from particles import Collision
from popups import Popup

pygame.init()

clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Mcgee")
vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

player = Player(WIDTH//2, HEIGHT//2)
bullets = []
particles = []
enemies = []
popups = []

shake_strength = 0
wave =1
wave_timer = 0
wave_delay = 120

def create_vignette(surface):
    width, height = surface.get_size()
    center_x, center_y = width //2, height // 2

    for x in range(width):
        for y in range(height):
            dx = x - center_x
            dy = y - center_y
            distance = (dx*dx + dy*dy) ** 0.5

            alpha = min(200, int(distance / 2))
            surface.set_at((x,y), (0,0,0, alpha))

def spawn_wave(wave):
    new_enemies = []

    speed = 1 + wave * 0.2
    health = 1 + wave // 3

    for _ in range(wave * 3):
        x = random.choice([0, WIDTH])
        y = random.randint (0, HEIGHT)

        new_enemies.append(Enemy(x, y))
    return new_enemies

#Main loop
create_vignette(vignette)
wave_in_progress = False
running = True
while running:

    if not wave_in_progress:
        wave_timer += 1
        if wave_timer >= wave_delay:
            popups.append(Popup(WIDTH//2 - 25, HEIGHT-500, f"WAVE: {wave}"))
            enemies = spawn_wave(wave)
            wave_in_progress = True
            wave_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullets.append(Bullet(player.pos.x, player.pos.y, mouse_x, mouse_y))

    player.update()
#------Enemy------
    for enemy in enemies:
        enemy.update(player.pos)
    
    if wave_in_progress and len(enemies) == 0:
        wave += 1
        wave_in_progress = False

#------Bullets------
    for bullet in bullets:
        bullet.update()

#------Popups------
    for popup in popups:
        popup.update()
    
    popups = [p for p in popups if not p.is_dead()]
      
#------Collisions------
    new_enemies = []
    new_bullets = []

    for enemy in enemies:
        hit = False

        for bullet in bullets:
            if bullet.pos.distance_to(enemy.pos) < enemy.radius:
                shake_strength = 8

                for _ in range(12):
                    particles.append(Collision(enemy.pos.x, enemy.pos.y))

                popups.append(Popup(enemy.pos.x, enemy.pos.y, "+100"))
                hit = True
                break
        if not hit:
            new_enemies.append(enemy)

    for bullet in bullets:
        hit_any = False

        for enemy in enemies:
            if bullet.pos.distance_to(enemy.pos) < enemy.radius:
                hit_any = True
                break
        if bullet.hit_wall(WIDTH, HEIGHT):
            for _ in range(10):
                particles.append(Collision(bullet.pos.x, bullet.pos.y))
            hit_any = True
        if not hit_any:
            new_bullets.append(bullet)
    
    bullets = new_bullets
    enemies = new_enemies
 
#------Particles------
    for particle in particles:
        particle.update()
    
    particles = [p for p in particles if not p.is_dead()]

#------Camera------
    offset_x = random.uniform(-shake_strength, shake_strength)
    offset_y = random.uniform(-shake_strength, shake_strength)

#------Drawing------
    screen.fill((30,30,30))

    player.draw(screen, offset_x, offset_y)
    for bullet in bullets:
        bullet.draw(screen, offset_x, offset_y)
    
    for particle in particles:
        particle.draw(screen, offset_x, offset_y)

    for enemy in enemies:
        enemy.draw(screen, offset_x, offset_y)
  
    for popup in popups:
        popup.draw(screen)

    screen.blit(vignette, (0,0))

    shake_strength *= 0.9
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
