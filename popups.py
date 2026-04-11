import pygame

class Popup:
    def __init__(self, x, y, text):
        self.pos = pygame.math.Vector2(x, y)
        self.text = text

        self.font = pygame.font.SysFont(None, 28)
        self.life = 60
        self.velocity = pygame.math.Vector2(0, -1)
        self.colour = (220,220,220)
    
    def update(self):
        self.pos += self.velocity
        self.life -= 1
    
    def draw(self, screen):
        img = self.font.render(self.text, True, self.colour)
        screen.blit(img, (self.pos.x, self.pos.y))
    
    def is_dead(self):
        return self.life <= 0