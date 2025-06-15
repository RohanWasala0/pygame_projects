from pygame import Color
from typing import Tuple

WIDTH: int = 640
HEIGHT: int = 672
SCREEN_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)

file_content = open('./assets/not-a-bauhaus-a-bauhome.hex')

color_palette = [Color("#"+color.strip()) for color in file_content if color.strip() and color.strip() != ""]