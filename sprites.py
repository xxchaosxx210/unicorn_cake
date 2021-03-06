import pygame
import os
import random
from collections import namedtuple

import graphics
import py_text
from graphics import SCREEN_WIDTH, SCREEN_HEIGHT
import sfx
from spritesheet import SpriteSheet
from spritesheet import load_rects

CAT = 0
DOG = 1
UNICORN = 2
DEAD_UNICORN = 3

IMAGE_PATH = f".{os.path.sep}images" 


class CakeScore(py_text.Text):
    
    def __init__(self, score, size):
        super(CakeScore, self).__init__(f"Cakes: {score}", size)
        self.score = score
        self.set_xy()
    
    def set_xy(self):
        self.rect.x = SCREEN_WIDTH - self.rect.width - 20
        self.rect.y = 10
    
    def inc_score(self):
        self.score += 1
        self.set_text(f"Cakes: {self.score}")
        self.set_xy()
    
    def reset_score(self):
        self.score = 0
        self.set_text(f"Cakes: {self.score}")
        self.set_xy()
        

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
    
    def draw(self, screenbuffer):
        screenbuffer.blit(self.surf, self.rect)
            
            
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
                if _enemy.sprite_id == DOG:
                    sfx.dog_bark.play()
                else:
                    sfx.cat_meow.play()
                self.kill()
                _enemy.kill()
        if self.rect.left > SCREEN_WIDTH:
            self.kill()
    
    def draw(self, screenbuffer):
        screenbuffer.blit(self.surf, self.rect)    
        

class AnimatedSprite(pygame.sprite.Sprite):
    
    def __init__(self, 
                 sheet_path,  
                 frame_change,
                 rects,
                 sprite_id):
        super(AnimatedSprite, self).__init__()
        sheet = SpriteSheet(sheet_path)
        self.surfs = sheet.images_at(rects, graphics.TRANSPARENT)
        self.walk_count = 0
        self.frame_change = frame_change
        self.frame_count = 0
        self.sprite_id = sprite_id
        self.sprite_count = len(self.surfs)
    
    def draw(self, screen_buffer):
        surf = self.surfs[self.walk_count]
        if self.sprite_id == DEAD_UNICORN:
            print(self.walk_count)
        x = self.rect.x
        y = self.rect.y
        self.rect = surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        screen_buffer.blit(surf, self.rect)
        if self.frame_count == self.frame_change:
            if self.walk_count == len(self.surfs)-1:
                self.walk_count = 0
            else:
                self.walk_count += 1
            self.frame_count = 0
        else:
            self.frame_count += 1


class DeadUnicorn(AnimatedSprite):
    
    def __init__(self, unicorn):
        path = ".\\images\\unicorn_sheet.png"
        width = 100
        height = 100
        y = 410
        rects = ((14, y, width, height), (117, y, width, height),
                 (219, y, width, height), (335, y, width, height),
                 (439, y, width, height), (552, y, width, height),
                 (656, y, width, height), (771, y, width, height),
                 (885, y, width, height))
        super(DeadUnicorn, self).__init__(path, 1, rects, DEAD_UNICORN)
        self.rect = self.surfs[0].get_rect(
            x = unicorn.rect.x,
            y = unicorn.rect.y
        )
        self.speed = 1
    
    def update(self):
        self.rect.move_ip(self.speed, 0)
            
class Unicorn(AnimatedSprite):   
    
    def __init__(self):
        path = ".\\images\\unicorn_sheet.png"
        width = 100
        height = 100
        y = 20
        rects = ((378, y, width, height),(484, y, width, height),
                 (581, y, width, height), (676, y, width, height),
                 (773, y, width, height), (874, y, width, height))
        super(Unicorn, self).__init__(path, 2, rects, UNICORN)
        self.rect = self.surfs[0].get_rect(
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


class Cat(AnimatedSprite):
    
    def __init__(self):
        path = os.path.join(IMAGE_PATH, "cat_sprite_sheet.png")
        rects = ((6, 0, 79, 75),
                 (88, 0, 79, 75),
                 (166, 0, 79, 75),
                 (243, 0, 79, 75),
                 (341, 0, 79, 75),
                 (433, 0, 79, 75),
                 (513, 0, 79, 75),
                 (600, 0, 79, 75)
        )
        super(Cat, self).__init__(path, 3, rects, CAT)
        self.speed = random.randint(5, 10)
        start_x = SCREEN_WIDTH + 100
        start_y = random.randint(0, SCREEN_HEIGHT)
        self.rect = self.surfs[0].get_rect(
            x = start_x,
            y = start_y
        )
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
   

class Dog(AnimatedSprite):
    def __init__(self):
        path = os.path.join(IMAGE_PATH, "dog_sprite_sheet.png")
        rects = ((20, 64, 94, 68), (109, 64, 94, 68),
                 (212, 64, 94, 68), (306, 64, 94, 68),
                 (404, 64, 94, 68), (490, 64, 94, 68),
                 (582, 64, 94, 68), (681, 64, 94, 68),
                 (778, 64, 94, 68), (874, 64, 94, 68))
        super(Dog, self).__init__(path, 3, rects, DOG)
        self.speed = random.randint(5, 10)
        start_x = SCREEN_WIDTH + 100
        start_y = random.randint(0, SCREEN_HEIGHT)
        self.rect = self.surfs[0].get_rect(
            x = start_x,
            y = start_y
        )
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
    
    def draw(self, screenbuffer):
        screenbuffer.blit(self.surf, self.rect)    
            
            
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
        
    def draw(self, screenbuffer):
        screenbuffer.blit(self.surf, self.rect)    