import pygame
import random
import time
import os

MAX_CAKES = 4

random.seed(time.time())

# prevents sound lag in game
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
pygame.mixer.init()

# init pygame first before importing files
import sprites
import graphics
import sfx
from graphics import SCREEN_WIDTH
from graphics import SCREEN_HEIGHT

clock = pygame.time.Clock()

screen_buffer = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Unicorn Princess by Ivy Snow Leeder(c) 2020")

ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 800)

ADD_CLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_CLOUD, 1000)

ADD_CAKE = pygame.USEREVENT + 3
pygame.time.set_timer(ADD_CAKE, 5000)


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
    screen_buffer.fill(graphics.SKY_BLUE)
    results_sound.play()
    screen_buffer.blit(text.surf, text.rect)
    pygame.display.update()
    time.sleep(timeout)
        
def game_loop():    
    unicorn = sprites.Unicorn()
    
    entities = {"enemies": pygame.sprite.Group(),
               "clouds": pygame.sprite.Group(),
               "stars": pygame.sprite.Group(),
               "cakes": pygame.sprite.Group(),
               "rainbow_powerups": pygame.sprite.Group(),
               "all": pygame.sprite.Group()}
    
    entities["all"].add(unicorn)
    
    cake_counter = CakeScore(0, 32)
    
    pygame.mixer.music.load(os.path.join(sfx.SOUND_PATH, "main.ogg"))
    pygame.mixer.music.play(loops=-1) 
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rainbow_star = sprites.RainbowStar(unicorn)
                    entities["all"].add(rainbow_star)
                    entities["stars"].add(rainbow_star)
            if event.type == ADD_ENEMY:
                enemy = sprites.Enemy()
                entities["enemies"].add(enemy)
                entities["all"].add(enemy)
            if event.type == ADD_CLOUD:
                cloud = sprites.Cloud()
                entities["clouds"].add(cloud)
                entities["all"].add(cloud)
            if event.type == ADD_CAKE:
                cake = sprites.UnicornCake()
                entities["cakes"].add(cake)
                entities["all"].add(cake)
                
        unicorn.update(pygame.key.get_pressed())         
        entities["enemies"].update()
        entities["stars"].update(entities["enemies"])
        entities["clouds"].update()
        entities["cakes"].update()
        entities["rainbow_powerups"].update()
        screen_buffer.fill(graphics.SKY_BLUE)
        screen_buffer.blit(cake_counter.surf, cake_counter.rect)
        for entity in entities["all"]:
            screen_buffer.blit(entity.surf, entity.rect)
        # update the score
        pygame.display.update()
        for _cake in entities["cakes"]:
            if pygame.sprite.collide_rect(unicorn, _cake):
                # play cake collection sound
                sfx.gulp.play()
                _cake.kill()
                cake_counter.inc_score()
                if cake_counter.score == MAX_CAKES:
                    # we won the challlenge!!
                    display_game_results("Congratulations!! You won the Unicorn Cake Challlenge!!!",
                                         sfx.game_over_voice, 4)
                    running = False
                elif cake_counter.score == 2:
                    rainbow_powerup = sprites.RainbowPowerup()
                    entities["rainbow_powerups"].add(rainbow_powerup)
                    entities["all"].add(rainbow_powerup)
        for powerup in entities["rainbow_powerups"]:
            if pygame.sprite.collide_rect(unicorn, powerup):
                sfx.powerup.play()
                powerup.kill()
                unicorn.speed += 20
        for enemy in entities["enemies"]:
            if pygame.sprite.collide_rect(unicorn, enemy):
                unicorn.kill()
                enemy.kill()
                display_game_results("You Lose!! :(", sfx.game_over_voice, 4)
                running = False            
        clock.tick(graphics.FRAME_RATE)

    unicorn.kill()
    entities["all"].empty()
    del entities["all"]
    del entities["clouds"]
    del entities["stars"]
    del entities["enemies"]
    del entities["cakes"]
    del cake_counter
    del unicorn
    pygame.mixer.music.stop()
    
def get_text(message, font_size):
    font = pygame.font.Font("unicorn.ttf", font_size)
    text = font.render(message, True, graphics.FONT_COLOUR, None)
    return text

def unicorn_selection_menu():
    running = True
    all_sprites = pygame.sprite.Group()
    unicorns = pygame.sprite.Group()
    while running:
        for event in pygame.event.get():
            if event.type == ADD_CLOUD:
                cloud = sprites.Cloud()
                all_sprites.add(cloud)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen_buffer.fill(graphics.SKY_BLUE)
        all_sprites.update()
        for entity in all_sprites:
            screen_buffer.blit(entity.surf, entity.rect)
        pygame.display.update()
        clock.tick(graphics.FRAME_RATE)
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
    
    pygame.mixer.music.load(os.path.join(sfx.SOUND_PATH, "menu.mp3"))
    pygame.mixer.music.play(loops=-1)
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    game_loop()
                    pygame.mixer.music.load(os.path.join(sfx.SOUND_PATH, "menu.mp3"))
                    pygame.mixer.music.play(loops=-1)
                if event.key == pygame.K_1:
                    unicorn_selection_menu()
            if event.type == ADD_CLOUD:
                cloud = sprites.Cloud()
                clouds.add(cloud)
                all_sprites.add(cloud)
                
        clouds.update()
        
        screen_buffer.fill(graphics.SKY_BLUE)
        for entity in all_sprites:
            screen_buffer.blit(entity.surf, entity.rect)
        screen_buffer.blit(title_text, title_rect)
        screen_buffer.blit(header2_text, header2_rect)
        screen_buffer.blit(header3_text, header3_rect)
        screen_buffer.blit(header4_text, header4_rect)
        pygame.display.update()
        clock.tick(graphics.FRAME_RATE)
    
main()
pygame.quit()