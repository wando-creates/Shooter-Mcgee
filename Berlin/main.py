import pygame
from player import Player

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Mcgee")

player = Player(WIDTH//2, HEIGHT//2)

#Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill((30,30,30))

    player.draw(screen)
    pygame.display.flip()
pygame.quit()
