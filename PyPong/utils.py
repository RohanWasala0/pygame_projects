from pygame import Color
from typing import Tuple

WIDTH: int = 640
HEIGHT: int = 480
SCREEN_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)

BLACK = Color(0,0,0)
BACKGROUND_BLACK = Color('#181C14')
PADDLE_BROWN = Color('#3C3D37')
BALL_GREY = Color('#697565')
PARTICLES_BEIGE = Color('#ECDFCC')

FONT_PATH = 'Assets/pixcel_font.ttf'

HIT = './Assets/hitHurt.ogg'
POINT = './Assets/explosion.ogg'