import pygame
import random
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from particles import Collision
from popups import Popup
from upgrades import paths, apply_upgrade
pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Mcgee")
vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 28)

pop_sound = pygame.mixer.Sound("sounds/popping.mp3")
pop_sound.set_volume(0.5)

state_change = pygame.mixer.Sound("sounds/state_change.mp3")
state_change.set_volume(0.8)

player = Player(WIDTH//2, HEIGHT//2)
game_state = "PLAY"

bullets = []
particles = []
enemies = []
popups = []

shake_strength = 0
wave =1
wave_timer = 0
wave_delay = 120
wave_score = 0
score = 1
score_scale = 1
display_score = 0


damage = 1


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
    types = ["red", "blue", "green", "yellow", "pink"]

    for _ in range(wave * 3):
        x = random.choice([0, WIDTH])
        y = random.randint (0, HEIGHT)

        max_index = min(len(types)-1, wave // 2)
        bloon_type = random.choice(types[:max_index+1])
        new_enemies.append(Enemy(x,y,bloon_type))

    return new_enemies



#Main loop
create_vignette(vignette)
wave_in_progress = False
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
                if game_state == "PLAY" and player.shoot_timer >= player.shoot_delay:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    player.shoot(bullets, mouse_x, mouse_y)
                    player.shoot_timer = 0
                    
        if game_state == "UPGRADING":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if player.path_choice is None:
                        apply_upgrade(player, "A")
                elif event.key == pygame.K_2:
                    if player.path_choice is None:
                        apply_upgrade(player, "B")
                elif event.key == pygame.K_RETURN:
                    game_state = "PLAY"
                    wave += 1
                    wave_in_progress = False
                    wave_timer = 0 


    if game_state == "PLAY":
        if not wave_in_progress:
            wave_timer += 1
            if wave_timer >= wave_delay:
                wave_score += wave * 50
                popups.append(Popup(WIDTH//2 - 36, HEIGHT-500, f"ROUND: {wave}"))
                popups.append(Popup(WIDTH//2 - 36, HEIGHT-450, f"+ {wave_score}"))
                player.score += wave_score
                enemies = spawn_wave(wave)
                wave_in_progress = True
                wave_timer = 0

        player.update()
#------Enemy------
        for enemy in enemies:
            enemy.update(player.pos)
        
#------Bullets------
        for bullet in bullets:
            bullet.update(enemies)

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
                    pop_sound.play()
                    shake_strength = 6
                    for _ in range(8):
                        particles.append(Collision(enemy.pos.x, enemy.pos.y))

                    downgrade = {
                        "pink":"yellow",
                        "yellow":"green",
                        "green":"blue",
                        "blue":"red",
                    }

                    if enemy.type in downgrade:
                        new_type = downgrade[enemy.type]
                        new_enemies.append(Enemy(enemy.pos.x, enemy.pos.y, new_type))
                        popups.append(Popup(enemy.pos.x, enemy.pos.y, "+1"))
                    else:
                        player.score += 1
                        popups.append(Popup(enemy.pos.x, enemy.pos.y, "+1"))
                    hit = True
                    break
                
            if not hit:
                new_enemies.append(enemy)

        enemies = new_enemies
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

#------game states------
    if len(enemies) == 0 and wave_in_progress and game_state == "PLAY":
        wave_in_progress = False
        game_state = "UPGRADING"
        wave_timer += 1


#------Camera------
    offset_x = random.uniform(-shake_strength, shake_strength)
    offset_y = random.uniform(-shake_strength, shake_strength)
    shake_strength *= 0.9


#------Drawing------
    screen.fill((30,30,30))

    if game_state == "PLAY":
        player.draw(screen, offset_x, offset_y)
        for bullet in bullets:
            bullet.draw(screen, offset_x, offset_y)
        for particle in particles:
            particle.draw(screen, offset_x, offset_y)
        for enemy in enemies:
            enemy.draw(screen, offset_x, offset_y)
        for popup in popups:
            popup.draw(screen)

#------Upgrading------
    elif game_state == "UPGRADING":
        screen.fill((30, 75, 30))
        screen.blit(font.render("Upgrades  -  ENTER to continue", True, (255,255,255)), (200, 130))

        for i, path_key in enumerate(["A", "B"]):
            x = 100 + i * 300
            tier = player.path_tiers[path_key]
            path = paths[path_key]

            for j, upgrade in enumerate(path):
                y = 220 + j * 80
                bought = j < tier
                affordable = score >= upgrade["cost"]

                if bought:
                    colour = (100, 220, 100)
                    label = f"[OWNED] {upgrade["name"]}"
                elif affordable:
                    colour = (200,200,200)
                    label = f"[{i+1}] {upgrade["name"]}  ${upgrade["cost"]}"
                else:
                    colour = (100,100,100)
                    label = f"{upgrade["name"]}  ${upgrade["cost"]}"
                
                screen.blit(font.render(label, True, colour), (x,y))

#------Cash board------

    display_score += (player.score - display_score) * 0.1
    score_scale += (1 - score_scale) * 0.1

    board_width = 180
    max_board_width = 320

    board_target = board_width + int(display_score * 0.1)
    board_target = min(board_target, max_board_width)

    box_width = 180
    box_width += (board_target - box_width) * 0.1

    pygame.draw.rect(screen, (20,20,20), (5,5,int(box_width),100), border_radius=8)
    pygame.draw.rect(screen, (200,200,200), (5,5,int(box_width),100), 2, border_radius=8)
    screen.blit(vignette, (0,0))

    score_text = font.render(f"Cash: {int(display_score)}", True, (200,200,200))
    scaled_text = pygame.transform.scale(score_text, (int(score_text.get_width() * score_scale), int(score_text.get_height() * score_scale)))

    screen.blit(scaled_text, (10,10))

    shake_strength *= 0.9
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
