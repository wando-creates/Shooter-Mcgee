import pygame
import random
import math
from player import Player
from enemy import Enemy, Boss
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
pygame.display.set_caption("Lost Light")
vignette = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 28)
title_font = pygame.font.Font("fonts/LuckiestGuy-Regular.ttf", 64)

pop_sound = pygame.mixer.Sound("sounds/popping.mp3")
pop_sound.set_volume(0.2)

state_change = pygame.mixer.Sound("sounds/state_change.mp3")

soundtrack = pygame.mixer.Sound("sounds/Soundtrack.mp3")
soundtrack.set_volume(0.3)

upgrade_sound = pygame.mixer.Sound("sounds/upgrade.mp3")
upgrade_sound.set_volume(0.1)

player = Player(WIDTH//2, HEIGHT//2)
skip_button = pygame.Rect(WIDTH - 160, HEIGHT - 50, 150, 40)

game_state = "START"
auto_skip = False
boss_unlocked = False

bullets = []
particles = []
enemies = []
popups = []
menu_enemies = []
spawn_queue = []

shake_strength = 0
wave =1
wave_timer = 0
wave_delay = 120
wave_score = 0
score = 1
score_scale = 1
display_score = 0
spawn_timer = 0
spawn_delay = 20

hit_flash = 0

damage = 1
boss = None

def create_vignette(surface, player_pos):
    surface.fill((100,100,100,220))

    surface.blit(vignette_circle, (player_pos.x - vignette_circle.get_width()//2, player_pos.y - vignette_circle.get_height()//2))

def make_vignette(radius):
    size = radius * 2
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    for i in range(radius, 0, -1):
        alpha = int(220 * (1-i / radius))
        pygame.draw.circle(surface, (0,0,0,alpha), (radius, radius), i)
    
    return surface

vignette_circle = make_vignette(1600)

def spawn_wave(wave):
    new_enemies = []
    types = ["red", "blue", "green", "yellow", "pink"]

    for _ in range(wave * 5):
        x = random.choice([0, WIDTH])
        y = random.randint (0, HEIGHT)

        max_index = min(len(types)-1, wave // 2)
        bloon_type = random.choice(types[:max_index+1])
        new_enemies.append(Enemy(x,y,bloon_type))

    return new_enemies



#Main loop
soundtrack.play(-1)
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
                if skip_button.collidepoint(pygame.mouse.get_pos()):
                    auto_skip = not auto_skip

        if event.type == pygame.KEYDOWN:
            if game_state == "START":
                if event.key == pygame.K_RETURN:
                    game_state = "PLAY"

            elif game_state == "UPGRADING":
                if event.key == pygame.K_1:
                    if player.path_choice is None:
                        apply_upgrade(player, "A")
                        upgrade_sound.play()
                elif event.key == pygame.K_2:
                    if player.path_choice is None:
                        apply_upgrade(player, "B")
                        upgrade_sound.play()
                elif event.key == pygame.K_RETURN:
                    state_change.play()
                    game_state = "PLAY"
                    wave += 1
                    wave_in_progress = False
                    wave_timer = 0 
            elif game_state == "GAME_OVER":
                if event.key == pygame.K_r:
                    player = Player(WIDTH//2, HEIGHT//2)
                    bullets.clear()
                    enemies.clear()
                    particles.clear()
                    popups.clear()

                    wave = 1
                    player.score = 1
                    game_state = "PLAY"
                    wave_in_progress = False

    if game_state == "PLAY":
        if not wave_in_progress:
            wave_timer += 1

            if wave_timer >= wave_delay:
                wave_score += wave * 20
                popups.append(Popup(WIDTH//2 - 36, HEIGHT-500, f"ROUND: {wave}"))
                popups.append(Popup(WIDTH//2 - 36, HEIGHT-450, f"+ {wave_score}"))
                player.score += wave_score
                spawn_queue = spawn_wave(wave)
                enemies = []
                spawn_timer = 0

                wave_in_progress = True
                wave_timer = 0

                if wave == 2:
                    boss = Boss(0, HEIGHT // 2)
                if boss_unlocked and random.random() < 0.2:
                    boss = Boss(random.choice([0,WIDTH]), random.randint(100, HEIGHT - 100))

        player.update()
#------Enemy------
        for enemy in enemies:
            enemy.update(player.pos)
        
#------Bullets------
        for bullet in bullets:
            all_targets = enemies + ([boss] if boss else [])
            bullet.update(all_targets)

#------Popups------
        for popup in popups:
            popup.update()
        
        popups = [p for p in popups if not p.is_dead()]
        
#------Collisions------
        new_enemies = []
        new_bullets = []
        
        for enemy in enemies:
            if enemy.pos.distance_to(player.pos) < enemy.radius + player.size:
                if player.damage_cooldown == 0:
                    player.health -= 1
                    player.damage_cooldown = 120
                    shake_strength = 50
                    hit_flash = 50

            hit = False

            for bullet in bullets:
                if bullet.pos.distance_to(enemy.pos) < enemy.radius:
                    pop_sound.play()
                    shake_strength = 6
                    for _ in range(8):
                        particles.append(Collision(enemy.pos.x, enemy.pos.y, enemy.colour))

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

        enemies = new_enemies if new_enemies else enemies

        for bullet in bullets:
            hit_any = False

            for enemy in enemies:
                if bullet.pos.distance_to(enemy.pos) < enemy.radius:
                    hit_any = True
                    break
            if bullet.hit_wall(WIDTH, HEIGHT):
                for _ in range(10):
                    particles.append(Collision(bullet.pos.x, bullet.pos.y, (0,0,0)))
                hit_any = True
            if not hit_any:
                new_bullets.append(bullet)
        
        bullets = new_bullets
        enemies = new_enemies

        if boss:
            boss.update(player.pos)

            for bullet in bullets[:]:
                if bullet.pos.distance_to(boss.pos) < boss.radius:
                    boss.health -= 1
                    bullets.remove(bullet)
                    pop_sound.play()
                    shake_strength = 6
                    for _ in range(6):
                        particles.append(Collision(boss.pos.x, boss.pos.y, boss.colour))
                    if boss.health <= 0:
                        boss_unlocked = True
                        player.score += 100
                        popups.append(Popup(boss.pos.x, boss.pos.y, "+100"))
                        boss = None
                        shake_strength = 30
                    break
        
        if boss and boss.pos.distance_to(player.pos)< boss.radius + player.size:
            if player.damage_cooldown == 0:
                player.health -= 1
                player.damage_cooldown = 120
                shake_strength = 50
                hit_flash = 50
        
                
#------Particles------
        for particle in particles:
            particle.update()
        
        particles = [p for p in particles if not p.is_dead()]

#------game states------
    if len(enemies) == 0 and len(spawn_queue) == 0 and wave_in_progress and game_state == "PLAY" and not boss:
        wave_in_progress = False
        if auto_skip:
            wave += 1
            wave_in_progress = False
            wave_timer = 0
        else:
            game_state = "UPGRADING"
            state_change.play()
        wave_timer += 1

    if player.health <= 0:
        game_state = "GAME_OVER"
    
#------Camera------
    offset_x = random.uniform(-shake_strength, shake_strength)
    offset_y = random.uniform(-shake_strength, shake_strength)
    shake_strength *= 0.9


#------Drawing------
    screen.fill((30,30,30))

    vignette.fill((0,0,0,0))
    create_vignette(vignette, player.pos)
    screen.blit(vignette, (0,0))
    
    menu_timer = pygame.time.get_ticks()

    if game_state == "PLAY":

        if boss:
            boss.draw(screen, offset_x, offset_y)

        if spawn_queue:
            spawn_timer += 1
            if spawn_timer >= spawn_delay:
                spawn_timer = 0
                enemies.append(spawn_queue.pop(0))

        if hit_flash > 0:
            flash = pygame.Surface((WIDTH, HEIGHT))
            flash.fill((64,0,0))
            flash.set_alpha(int(hit_flash))
            screen.blit(flash, (0,0))

        player.draw(screen, offset_x, offset_y)
        colour = (0,180,80) if auto_skip else(80,80,80)
        pygame.draw.rect(screen,colour,skip_button, border_radius=8)
        screen.blit(font.render("Auto Skip", True, (255,255,255)), (WIDTH -150, HEIGHT - 42))
        heart = pygame.transform.scale(player.health_image, (32,32))

        for i in range(player.health):
            screen.blit(heart, (10 + i * 36, 115))
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
        screen.fill((64,0,0))
        screen.blit(font.render("Upgrades  -  ENTER to continue", True, (255,255,255)), (105, 120))
        screen.blit(font.render("Press 1", True, (255,255,255)), (105, 180))
        screen.blit(font.render("Press 2", True, (255,255,255)), (400, 180))

        for i, path_key in enumerate(["A", "B"]):
            x = 100 + i * 300
            tier = player.path_tiers[path_key]
            path = paths[path_key]

            for j, upgrade in enumerate(path):
                y = 220 + j * 80
                bought = j < tier
                affordable = player.score >= upgrade["cost"]

                if bought:
                    colour = (220,220,220)
                    label = f"OWNED {upgrade["name"]}"
                elif affordable:
                    colour = (50,200,50)
                    label = f"{i+1}: {upgrade["name"]}  ${upgrade["cost"]}"
                else:
                    colour = (100,100,100)
                    label = f"{upgrade["name"]}  ${upgrade["cost"]}"
                
                screen.blit(font.render(label, True, colour), (x,y))

    if hit_flash > 0:
        hit_flash *= 0.8
        if hit_flash < 1:
            hit_flash = 0

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

    score_text = font.render(f"Cash: {int(display_score)}", True, (200,200,200))
    scaled_text = pygame.transform.scale(score_text, (int(score_text.get_width() * score_scale), int(score_text.get_height() * score_scale)))

    round_text = font.render(f"Round: {int(wave)}", True, (200,200,200))

    screen.blit(scaled_text, (10,10))
    screen.blit(round_text, (10,45))

    shake_strength *= 0.9

    if game_state == "START":
        screen.fill((20,20,30))
        alpha = 150 + int(100 * math.sin(menu_timer * 0.003))
        bg = 20 + int(10 * math.sin(menu_timer * -0.003))
        screen.fill((bg,bg,bg))

        if random.random() < 0.02:
            y = random.randint(0, HEIGHT)

            if random.random() < 0.5:
                x = -50
                direction = 1
            else:
                x = WIDTH + 50
                direction = -1
            enemy = Enemy(x,y, random.choice(["red", "blue", "green", "yellow", "pink"]))
            enemy.menu_direction = direction
            menu_enemies.append(enemy)
        
        for enemy in menu_enemies:
            enemy.pos.x += enemy.menu_direction * enemy.speed
            enemy.animate()

        menu_enemies = [
            e for e in menu_enemies
            if -100 < e.pos.x < WIDTH + 100
        ]

        for enemy in menu_enemies:
            enemy.draw(screen)

        title = title_font.render("Lost Light", True, (alpha,alpha,alpha))
        subtitle = font.render("Press ENTER To Start", True, (64,0,0))

        screen.blit(title, (WIDTH//2 - title.get_width()//2, 180))
        screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 280))

    elif game_state == "GAME_OVER":
        screen.fill((255,255,255))
        screen.blit(font.render("GAME OVER", True, (64,0,0)), (290, 248))
        screen.blit(font.render("Press R To Restart", True, (64,0,0)), (290, 288))


    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
