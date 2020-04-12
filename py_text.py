import pygame
import graphics

def get_text(message, font_size):
    font = pygame.font.Font("unicorn.ttf", font_size)
    text = font.render(message, True, graphics.FONT_COLOUR, None)
    return text

class Text:
    
    def __init__(self, message, size):
        self.size = size
        self.font = pygame.font.Font("unicorn.ttf", size)
        self.set_text(message)
    
    def set_text(self, text):
        self.text = text
        self.surf = self.font.render(text, True, graphics.FONT_COLOUR, None)
        self.rect = self.surf.get_rect()
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def center(self):
        self.rect.center = (graphics.SCREEN_WIDTH // 2, graphics.SCREEN_HEIGHT // 2)