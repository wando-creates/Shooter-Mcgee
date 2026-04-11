import pygame
from player import Player
from bullet import Bullet
from particles import Collision

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Mcgee")

player = Player(WIDTH//2, HEIGHT//2)
bullets = []
particles = []

#Main loop
running = True
while running:
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
    new_bullets = []
    for bullet in bullets:
        bullet.update()

        if bullet.hit_wall(WIDTH, HEIGHT):
            for _ in range(10):
                particles.append(Collision(bullet.pos.x, bullet.pos.y))
            else:
                new_bullets.append(bullet)
           
    bullets = [bullet for bullet in bullets
               if not bullet.hit_wall(WIDTH, HEIGHT)]
    
    for particle in particles:
        particle.update()
    
    particles = [p for p in particles if not p.is_dead()]

    screen.fill((30,30,30))

    player.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)
    
    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()
pygame.quit()
