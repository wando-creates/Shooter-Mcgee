import pygame
import random
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from particles import Collision
from popups import Popup

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
shop_timer = 0
shop_delay = 120
going_to_shop = False

damage = 1

shop_buttons = [{"rect": pygame.Rect(100,200,250,60), "text": "Damage +1", "cost": 100, "action": "damage"},
                {"rect": pygame.Rect(100,280,250,60), "text": "Speed +0.2", "cost": 100, "action": "speed"}]

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

def handle_shop_click(pos):
    global score, damage

    for button in shop_buttons:
        if button["rect"].collidepoint(pos):
            if score >= button["cost"]:
                score -= button["cost"]

                if button["action"] == "damage":
                    damage += 1
                    button["cost"] += 50
                
                if button["action"] == "speed":
                    player.speed += 0.2
                    button["cost"] += 50
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
            if event.key == pygame.K_RETURN and game_state == "SHOP":
                state_change.play()
                game_state = "PLAY"
                wave_in_progress = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if game_state == "PLAY":
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    bullets.append(Bullet(player.pos.x, player.pos.y, mouse_x, mouse_y))
                elif game_state == "SHOP":
                    handle_shop_click(pygame.mouse.get_pos())
    
    if game_state == "PLAY":
        if not wave_in_progress:
            wave_timer += 1
            if wave_timer >= wave_delay:
                wave_score += wave * 50
                popups.append(Popup(WIDTH//2 - 36, HEIGHT-500, f"ROUND: {wave}"))
                popups.append(Popup(WIDTH//2 - 36, HEIGHT-450, f"+ {wave_score}"))
                score += wave_score
                enemies = spawn_wave(wave)
                wave_in_progress = True
                wave_timer = 0

        player.update()
#------Enemy------
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
                        score += 1
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

#------Game states------
        if game_state == "PLAY":
            if wave_in_progress and len(enemies) == 0 and not going_to_shop:
                going_to_shop = True
                shop_timer = 0

    if going_to_shop:
        shop_timer += 1

        for particle in particles:
            particle.update()
        particles = [p for p in particles if not p.is_dead()]
        
        for popup in popups:
            popup.update()
        popups = [p for p in popups if not p.is_dead()]

        if shop_timer >= shop_delay:
            state_change.play()
            game_state = "SHOP"
            going_to_shop = False
            wave_in_progress = False
            wave += 1

    elif game_state == "SHOP":
        pass

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

    elif game_state == "SHOP":
        mouse_pos = pygame.mouse.get_pos()
        screen.fill((30,75,30))

        title = font.render("SHOP - PRESS ENTER TO CONTINUE", True, (255,255,255))
        screen.blit(title, (250, 50))

        for button in shop_buttons:

            if button["rect"].collidepoint(mouse_pos):
                colour = (80,80,80)
            else:
                colour = (40,40,40)
            
            if score < button["cost"]:
                colour = (25,25,25)

            pygame.draw.rect(screen, (40,40,40), button["rect"], border_radius=8)
            pygame.draw.rect(screen, (200,200,200), button["rect"], 2, border_radius=8)

            text = font.render(f"{button['text']} (${button['cost']})", True, (255,255,255))
            screen.blit(text, (button["rect"].x + 10, button["rect"].y + 15))
        

#------Cash board------

    display_score += (score - display_score) * 0.1
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
