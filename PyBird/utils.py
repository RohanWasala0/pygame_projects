from pygame import Color, image
import os
from typing import Tuple

WIDTH: int = 720
HEIGHT: int = 450
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
FOLIAGE = []
BIRD_IDLE, BIRD_FLAP = [], []

for entry in os.scandir('./assets/Retro-Lines-16x16/Bird/idle/'):
    BIRD_IDLE.append(image.load(entry.path))
for entry in os.scandir('./assets/Retro-Lines-16x16/Bird/flap/'):
    BIRD_FLAP.append(image.load(entry.path))

for entry in os.scandir('./assets/Retro-Lines-16x16/background_air'):
    BACKGROUND_AIR.append(image.load(entry.path))

for entry in os.scandir('./assets/Retro-Lines-16x16/ground_tiles'):
    GROUND.append(image.load(entry.path))

for entry in os.scandir('./assets/Retro-Lines-16x16/foliage'):
    FOLIAGE.append(image.load(entry.path))

file = open('./assets/Retro-Lines-16x16/autotile_tilemap/mask.txt').readlines()

TILE_MASK = [[int(char) for char in line.strip()] for line in file[:5]]
# MASKS = list(map(lambda x: list(map(lambda x: int(x), list(x.replace("\n", "").replace(" ", "")))), file[5:]))
MASKS = [[int(char) for char in line.replace("\n", "").replace(" ", "")] for line in file[6:]]
# print(MASKS)
TILE_SET = image.load('./assets/Retro-Lines-16x16/autotile_tilemap/tilemap.png')