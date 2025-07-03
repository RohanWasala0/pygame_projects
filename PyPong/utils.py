from pygame import Color, image, Vector2, Surface, SRCALPHA
from typing import Tuple

WIDTH: int = 640
HEIGHT: int = 480
SCREEN_SIZE: Tuple[int, int] = (WIDTH, HEIGHT)

BLACK = Color(0,0,0)
BACKGROUND_BLACK = Color('#181C14')
PADDLE_BROWN = Color('#3C3D37')
BALL_GREY = Color('#697565')
PARTICLES_BEIGE = Color('#ECDFCC')

FONT_PATH = 'Assets/pixel_font.ttf'
FONT_PATH_04b = 'Assets/04B_03__.ttf'

HIT = './Assets/hitHurt.ogg'
POINT = './Assets/explosion.ogg'

space_key = image.load('./Assets/Space_key.png')
escape_key = image.load('./Assets/escap_key.png')
logo = image.load("./Assets/logo.png")
def make_tile_surface(
    position: Vector2,
    scale: float = 1,
) -> Surface:
    """Cuts, Scales a Surface from the tilemap to make tile sprite 
    Returns:
        Surface: The tile sprite as a surface scaled to factor 
    """
    x, y = position.x* 16, position.y* 16
    tile: Surface = Surface((16, 16), SRCALPHA)
    tile.blit(
        keyboard,
        (0, 0),
        (x, y, 16, 16)
    )
    # return transform.scale(tile, (tile.width* scale, tile.height* scale))0
    return tile
keyboard =  image.load('./Assets/Keyboard Letters and Symbols normal .png')
keyboard_keys = []
for y in range(7):
    for x in range(8):
        key = make_tile_surface(Vector2(x, y))
        keyboard_keys.append(key)
