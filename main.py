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

player = Player(WIDTH//2, HEIGHT//2)
bullets = []
particles = []
enemies = []
popups = []

#Main loop
running = True
while running:

    if random.randint(1,60) == 1:
        side = random.randint(1, 4)

        if side == 1:
            x, y = 0, random.randint(0, HEIGHT)
        elif side == 2:
            x, y = WIDTH, random.randint(0, HEIGHT)
        elif side == 3:
            x, y = random.randint(0, WIDTH), 0
        else:
            x, y = random.randint(0, WIDTH), HEIGHT
        
        enemies.append(Enemy(x, y))

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
    new_enemies = []
    new_bullets = []

    for enemy in enemies:
        enemy.update(player.pos)

#------Bullets------
    for bullet in bullets:
        bullet.update()

#------Popups------
    for popup in popups:
        popup.update()
    
    popups = [p for p in popups if not p.is_dead()]
      
#------Collisions------
    for enemy in enemies:
        enemy_alive = True

        for bullet in bullets:
            dist = math.hypot(enemy.pos.x - bullet.pos.x,
                              enemy.pos.y - bullet.pos.y)
            
            if dist < enemy.radius + bullet.radius:
                for _ in range(12):
                    particles.append(Collision(enemy.pos.x, enemy.pos.y))
                popups.append(Popup(enemy.pos.x, enemy.pos.y, "+100"))
                enemy_alive = False
                break

        if enemy_alive:
            new_enemies.append(enemy)

    enemies = new_enemies

    for bullet in bullets:
        if bullet.hit_wall(WIDTH, HEIGHT):
            for _ in range(10):
                particles.append(Collision(bullet.pos.x, bullet.pos.y))
        else:
            new_bullets.append(bullet)
    
    bullets = new_bullets
    
#------Particles------
    for particle in particles:
        particle.update()
    
    particles = [p for p in particles if not p.is_dead()]

    screen.fill((30,30,30))

    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    
    for particle in particles:
        particle.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)
  
    for popup in popups:
        popup.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
