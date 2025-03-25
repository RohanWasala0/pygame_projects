from pygame import Color, image
import os
from typing import Tuple

WIDTH: int = 640
HEIGHT: int = 480
SCREEN_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)

BLACK = Color(0,0,0)
BACKGROUND_BLACK = Color('#181C14')
PADDLE_BROWN = Color('#3C3D37')
BALL_GREY = Color('#697565')
PARTICLES_BEIGE = Color('#ECDFCC')

FONT_PATH = 'assets/pixcel_font.ttf'
ENVIRONMENT_SHEET = image.load('assets/Retro-Lines-16x16/Environment.png')
BIRD_SHEET = image.load('assets/Retro-Lines-16x16/bird.png')
BACKGROUND_AIR = []
GROUND = []

for entry in os.scandir('./assets/Retro-Lines-16x16/background_air'):
    BACKGROUND_AIR.append(image.load(entry.path))

for entry in os.scandir('./assets/Retro-Lines-16x16/ground_tiles'):
    GROUND.append(image.load(entry.path))
