from pygame import (
        sprite, 
        Vector2, 
        draw, 
        Color, 
        Surface, 
        Rect, 
        math, 
        display, 
        SRCALPHA,
        mask,
    ) 
from typing import Tuple, Optional

from utils import FONT_PATH
from text_canvas import text_canvas
from input_manager import InputManager

class Settings(sprite.Sprite):
    def __init__(
        self, 
        groups: sprite.Group = {},
        anchor: str = 'topleft',
        color: Color = Color('black'),
        position: Optional[Vector2] = Vector2(), 
        dimensions: Tuple[int, int] = (0, 0), 
    ):
        super().__init__(groups)
        
        self.color = color
        self.group = groups
        self.anchor = anchor
        self.position = position 
        self.dimensions = dimensions

        self.input_manager = InputManager()
        self.input_manager.input_chart = {}

        self.canvas_group = sprite.Group()
        self._initialize_text()

        self.render()

    def update(self, deltaTime: float):
        self.canvas_group.update(deltaTime)
        self.render()

    def render(self):

        self.image = Surface(self.dimensions, SRCALPHA) if self.dimensions != (0, 0) else Surface((5, 5), SRCALPHA)
        self.image.set_colorkey(Color('black'))
        self.image.fill(Color('black'))
        self.image.fill(self.color)

        # self.debug(16, self.image)
        self.canvas_group.draw(self.image)

        self.rect: Rect = self.image.get_rect()
        self.mask: mask.Mask = mask.from_surface(self.image)
        setattr(self.rect, self.anchor, self.position)

    def _initialize_text(self,) -> None:
        self.music_text = text_canvas(
            raw= f"[position: 32, 32][size: 64][text: PyPong]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
            # anchor= 'center'
        )
        self.play_text = text_canvas(
            raw=f"[position: 32, 64 + 32 + 32][size: 32][text: PLAY][effect: text_sin]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
        )
        self.controls_text = text_canvas(
            raw=f"[position: 32, (64+32+32)+32+16][size: 32][text: CONTROLS]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
        )
        self.quit = text_canvas(
            raw= f"[position: 32, (64+32+32+32)+32+16+16][size: 32][text: QUIT]",
            groups= self.canvas_group,
            font_path= FONT_PATH,
        )

    def debug(self, spacing, grid_surface):
        draw.rect(
            grid_surface,
            Color('white'),
            grid_surface.get_rect(),
            width= 1,
        )

        width, height = self.dimensions
        grid_color = Color('white')
        for x in range(0, width, spacing):
            draw.line(grid_surface, grid_color, (x, 0), (x, height)) 
        for y in range(0, height, spacing):
            draw.line(grid_surface, grid_color, (0, y), (width, y)) 