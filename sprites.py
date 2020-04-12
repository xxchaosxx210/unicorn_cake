import pygame
import os
import random

import graphics
from graphics import SCREEN_WIDTH, SCREEN_HEIGHT
import sfx

CAT = 0
DOG = 1

IMAGE_PATH = f".{os.path.sep}images" 

class Cloud(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "cloud.png")).convert()
        self.surf.set_colorkey(graphics.TRANSPARENT, pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 
                      random.randint(0, SCREEN_HEIGHT))
        )
        self.speed = 5
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
            
class RainbowStar(pygame.sprite.Sprite):
    
    def __init__(self, _entity):
        super(RainbowStar, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "star.png")).convert()
        self.surf.set_colorkey(graphics.TRANSPARENT, pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            left = _entity.rect.right,
            top = _entity.rect.top + 10
        )
        self.speed = 10
    
    def update(self, _enemies):
        self.rect.move_ip(self.speed, 0)
        for _enemy in _enemies:
            if pygame.sprite.collide_rect(self, _enemy):
                if _enemy.type == "cat":
                    sfx.cat_meow.play()
                else:
                    sfx.dog_bark.play()
                self.kill()
                _enemy.kill()
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
            
            
class Unicorn(pygame.sprite.Sprite):   
    
    def __init__(self):
        super(Unicorn, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "unicorn.png")).convert()
        self.surf.set_colorkey(graphics.TRANSPARENT, pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            top = 0,
            left = 0
        )
        self.speed = 10
        self.cakes = 0
    
    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
            
class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Enemy, self).__init__()
        if random.randint(0, 1) == CAT:
            self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "cat.png")).convert()
            self.type = "cat"
        else:
            self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "dog.png")).convert()
            self.type = "dog"
        self.surf.set_colorkey(graphics.TRANSPARENT, pygame.RLEACCEL)
        start_x = SCREEN_WIDTH + 100
        start_y = random.randint(0, SCREEN_HEIGHT)
        self.rect = self.surf.get_rect(
            right = start_x,
            bottom = start_y
        )
        self.speed = random.randint(3, 20)
        if random.randint(0, 1) == 1:
            self.is_moving_down = True
        else:
            self.is_moving_down = False
        
    def update(self):
        if self.rect.top < 0:
            self.rect.top = 0
            self.is_moving_down = True
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.is_moving_down = False
        
        if self.is_moving_down:
            self.rect.move_ip(-self.speed, +self.speed)
        else:
            self.rect.move_ip(-self.speed, -self.speed)
        if self.rect.right < 0:
            self.kill()
            
            
class RainbowPowerup(pygame.sprite.Sprite):
    
    def __init__(self):
        super(RainbowPowerup, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "rainbow_powerup.png")).convert()
        self.surf.set_colorkey(graphics.TRANSPARENT, pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.x = SCREEN_WIDTH + 50
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = 3
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            
            
class UnicornCake(pygame.sprite.Sprite):
    
    def __init__(self):
        super(UnicornCake, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "unicorn_cake.png")).convert()
        self.surf.set_colorkey(graphics.TRANSPARENT, pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect.center = (SCREEN_WIDTH + 20, random.randint(0, SCREEN_HEIGHT))
        
        self.is_moving_down = True
        self.speed = random.randint(12, 25)
    
    def update(self):        
        if self.rect.top < 0:
            self.rect.top = 0
            self.is_moving_down = True
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.is_moving_down = False
        
        if self.is_moving_down:
            self.rect.move_ip(-self.speed, +self.speed)
        else:
            self.rect.move_ip(-self.speed, -self.speed)
        if self.rect.right < 0:
            self.kill() 