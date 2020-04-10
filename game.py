import pygame
import random
import time
import os
from collections import namedtuple

MAX_CAKES = 4

CAT = 0
DOG = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

FRAME_RATE = 30

WHITE = (255, 255, 255)
FONT_COLOUR = (255, 0, 220)
SKY_BLUE = (150, 150, 255)
TRANSPARENT = (127, 255, 255)

ID_UNICORN_ONE = 1001
ID_UNICORN_TWO = 1002

random.seed(time.time())

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

screen_buffer = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Unicorn Princess by Ivy Snow Leeder(c) 2020")

ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 800)

ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

ADD_CAKE = pygame.USEREVENT + 3
pygame.time.set_timer(ADD_CAKE, 5000)

SOUND_PATH = f".{os.path.sep}sound"
IMAGE_PATH = f".{os.path.sep}images"

gl_sounds = namedtuple("Sfx", ["cat_meow", "dog_bark", "game_over_voice",
                               "died", "won", "cake_collect"])(
    pygame.mixer.Sound(os.path.join(SOUND_PATH, "cat.ogg")),
    pygame.mixer.Sound(os.path.join(SOUND_PATH, "dog.ogg")),
    pygame.mixer.Sound(os.path.join(SOUND_PATH, "gameover.ogg")),
    None,
    None,
    None
)


class Cloud(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "cloud.png")).convert()
        self.surf.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
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
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "stars.jpg")).convert()
        self.surf.set_colorkey(WHITE, pygame.RLEACCEL)
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
                    gl_sounds.cat_meow.play()
                else:
                    gl_sounds.dog_bark.play()
                self.kill()
                _enemy.kill()
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Unicorn(pygame.sprite.Sprite):
    
    def __init__(self, _type):
        super(Unicorn, self).__init__()
        if _type == ID_UNICORN_ONE:
            self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "unicorn.png")).convert()
        elif _type == ID_UNICORN_TWO:
            self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "unicorn2.png")).convert()
        self.surf.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
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
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Enemy, self).__init__()
        if random.randint(0, 1) == CAT:
            self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "cat.png")).convert()
            self.type = "cat"
        else:
            self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "dog.png")).convert()
            self.type = "dog"
        self.surf.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
        start_x = SCREEN_WIDTH + 100
        start_y = random.randint(0, SCREEN_HEIGHT)
        self.rect = self.surf.get_rect(
            right = start_x,
            bottom = start_y
        )
        self.speed = random.randint(3, 20)
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class UnicornCake(pygame.sprite.Sprite):
    
    def __init__(self):
        super(UnicornCake, self).__init__()
        self.surf = pygame.image.load(os.path.join(IMAGE_PATH, "unicorn_cake.jpg")).convert()
        self.surf.set_colorkey(TRANSPARENT, pygame.RLEACCEL)
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
            

class Text:
    
    def __init__(self, message, size):
        self.size = size
        self.font = pygame.font.Font("unicorn.ttf", size)
        self.set_text(message)
    
    def set_text(self, text):
        self.text = text
        self.surf = self.font.render(text, True, FONT_COLOUR, None)
        self.rect = self.surf.get_rect()
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def center(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        

class CakeScore(Text):
    
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
        

def display_game_results(text, results_sound, timeout):
    pygame.mixer.music.stop()
    text = Text(text, 42)
    text.center()
    screen_buffer.fill(SKY_BLUE)
    results_sound.play()
    screen_buffer.blit(text.surf, text.rect)
    pygame.display.update()
    time.sleep(timeout)
        
def game_loop():    
    unicorn = Unicorn(ID_UNICORN_ONE)
    
    sprites = {"enemies": pygame.sprite.Group(),
               "clouds": pygame.sprite.Group(),
               "stars": pygame.sprite.Group(),
               "cakes": pygame.sprite.Group(),
               "all": pygame.sprite.Group()}
    
    sprites["all"].add(unicorn)
    
    cake_counter = CakeScore(0, 32)
    
    pygame.mixer.music.load(os.path.join(SOUND_PATH, "main.mp3"))
    pygame.mixer.music.play(loops=-1) 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rainbow_star = RainbowStar(unicorn)
                    sprites["all"].add(rainbow_star)
                    sprites["stars"].add(rainbow_star)
            if event.type == ADD_ENEMY:
                enemy = Enemy()
                sprites["enemies"].add(enemy)
                sprites["all"].add(enemy)
            if event.type == ADD_CLOUD:
                cloud = Cloud()
                sprites["clouds"].add(cloud)
                sprites["all"].add(cloud)
            if event.type == ADD_CAKE:
                cake = UnicornCake()
                sprites["cakes"].add(cake)
                sprites["all"].add(cake)
                
        unicorn.update(pygame.key.get_pressed())         
        sprites["enemies"].update()
        sprites["stars"].update(sprites["enemies"])
        sprites["clouds"].update()
        sprites["cakes"].update()
        screen_buffer.fill(SKY_BLUE)
        screen_buffer.blit(cake_counter.surf, cake_counter.rect)
        for entity in sprites["all"]:
            screen_buffer.blit(entity.surf, entity.rect)
        # update the score
        pygame.display.update()
        for _cake in sprites["cakes"]:
            if pygame.sprite.collide_rect(unicorn, _cake):
                # play cake collection sound
                #gl_sounds.cake_collect.play()
                _cake.kill()
                cake_counter.inc_score()
                if cake_counter.score == MAX_CAKES:
                    # we won the challlenge!!
                    display_game_results("Congratulations!! You won the Unicorn Cake Challlenge!!!",
                                         gl_sounds.game_over_voice, 4)
                    running = False
        if pygame.sprite.spritecollideany(unicorn, sprites["enemies"]):
            unicorn.kill()
            display_game_results("You Lose!! :(", gl_sounds.game_over_voice, 4)
            running = False
        clock.tick(FRAME_RATE)

    unicorn.kill()
    sprites["all"].empty()
    del sprites["all"]
    del sprites["clouds"]
    del sprites["stars"]
    del sprites["enemies"]
    del sprites["cakes"]
    del cake_counter
    del unicorn
    pygame.mixer.music.stop()
    
def get_text(message, font_size):
    font = pygame.font.Font("unicorn.ttf", font_size)
    text = font.render(message, True, FONT_COLOUR, None)
    return text

def unicorn_selection_menu():
    running = True
    all_sprites = pygame.sprite.Group()
    unicorns = pygame.sprite.Group()
    while running:
        for event in pygame.event.get():
            if event.type == ADD_CLOUD:
                cloud = Cloud()
                all_sprites.add(cloud)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen_buffer.fill(SKY_BLUE)
        all_sprites.update()
        for entity in all_sprites:
            screen_buffer.blit(entity.surf, entity.rect)
        pygame.display.update()
        clock.tick(FRAME_RATE)
    all_sprites.empty()
    unicorns.empty()
    del all_sprites

def main():
    running = True
    
    title_text = get_text("Unicorn Cake Game(c)", 64)
    title_rect = title_text.get_rect()
    title_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - title_rect.height)
    
    header2_text = get_text("Coded by Paul Millar", 43)
    header3_text = get_text("Designed by Ivy Snow Leeder", 43)
    header4_text = get_text("Press 'Return' key to Play.", 32)
    
    header2_rect = header2_text.get_rect()
    header2_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    
    header3_rect = header3_text.get_rect()
    header3_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + header2_rect.height)
    
    current_y_pos = (SCREEN_HEIGHT // 2) + header3_rect.height
    current_y_pos += header3_rect.height + 20
    header4_rect = header4_text.get_rect()
    header4_rect.center = (SCREEN_WIDTH // 2, current_y_pos)
    
    clouds = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    
    pygame.mixer.music.load(os.path.join(SOUND_PATH, "menu.mp3"))
    pygame.mixer.music.play(loops=-1)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    game_loop()
                    pygame.mixer.music.load(os.path.join(SOUND_PATH, "menu.mp3"))
                    pygame.mixer.music.play(loops=-1)
                if event.key == pygame.K_1:
                    unicorn_selection_menu()
            if event.type == ADD_CLOUD:
                cloud = Cloud()
                clouds.add(cloud)
                all_sprites.add(cloud)
                
        clouds.update()
        
        screen_buffer.fill(SKY_BLUE)
        for entity in all_sprites:
            screen_buffer.blit(entity.surf, entity.rect)
        screen_buffer.blit(title_text, title_rect)
        screen_buffer.blit(header2_text, header2_rect)
        screen_buffer.blit(header3_text, header3_rect)
        screen_buffer.blit(header4_text, header4_rect)
        pygame.display.update()
        clock.tick(FRAME_RATE)
    
main()
pygame.quit()