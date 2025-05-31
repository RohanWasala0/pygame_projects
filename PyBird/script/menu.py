from random import choice, randrange
from pygame import sprite, Vector2, Event, Rect, Color, Surface, SRCALPHA, draw, transform
from pygame import KEYDOWN, K_SPACE, event, USEREVENT
from typing import Dict, Optional, Any, Tuple
from .text_canvas import text_canvas

class Menu(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                font_path: str,
                position: Optional[Vector2] = None, 
                dimensions: Tuple[int, int] = (5, 5),
                color: Color = Color('white'),
                background_color: Color = Color('black'),
                anchor: str = 'topleft',
                debug: bool = False,
                ) -> None:
        """Initialize environment sprite

        Args:
            groups (sprite.Group): Pygame sprite group(s) that this belongs to 
            position (Optional[Vector2], optional): Starting position of this sprite. Defaults to None.
            anchor (str, optional): Position anchor point. Defaults to 'topleft'.
            debug (bool, optional): Whether to draw a debug box around the sprite. Defaults to False.
        """
        super().__init__(groups)
        
        self.anchor: str = anchor
        self.color: Color = color
        self.group: sprite.Group = groups
        self.dimension: Tuple[int, int] = dimensions
        self.background_color: Color = background_color
        self.position: Vector2 = position or Vector2(0, 0)
        
        self.canvas = sprite.Group()
        text_canvas(
            groups= self.canvas,
            font_path= font_path,
            font_size= 25,
            text= 'MENU'
        )
        self.render(debug)

    def update(self, deltaTime: float):
        self.canvas.update(deltaTime)
        self.render()
    
    def render(
        self,
        _debug_: bool = False,
    ):
        self.image: Surface = Surface(self.dimension)
        self.image.fill(self.background_color)

        self.image.blit(self._debug(16), (0, 0)) if _debug_ else None
        self.canvas.draw(self.image)

        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def _debug(
        self,
        spacing: int,
    ) -> Surface:
        debug_surface: Surface = Surface(self.image.size, SRCALPHA)
        grid_color: Color = Color(173, 170, 170, 75),    
        WIDTH, HEIGHT = self.image.size
        for x in range(0, WIDTH, spacing):
            draw.line(debug_surface, grid_color, (x, 0), (x, HEIGHT)) 
        for y in range(0, HEIGHT, spacing):
            draw.line(debug_surface, grid_color, (0, y), (WIDTH, y)) 
        
        draw.rect(
            debug_surface, 
            Color('white'),
            debug_surface.get_rect(),
            width=1,
        ) 
        return debug_surface