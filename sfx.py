import pygame
import os

SOUND_PATH = f".{os.path.sep}sound"

cat_meow = pygame.mixer.Sound(os.path.join(SOUND_PATH, "cat.ogg"))
dog_bark = pygame.mixer.Sound(os.path.join(SOUND_PATH, "dog.ogg"))
game_over_voice = pygame.mixer.Sound(os.path.join(SOUND_PATH, "gameover.ogg"))
gulp = pygame.mixer.Sound(os.path.join(SOUND_PATH, "gulp.ogg"))
powerup = pygame.mixer.Sound(os.path.join(SOUND_PATH, "powerup.ogg"))
level_complete = pygame.mixer.Sound(os.path.join(SOUND_PATH, "level_complete.ogg"))