from random import choice, randrange
from pygame import sprite, Vector2, Event, Rect, Color, Surface, SRCALPHA, draw, transform
from pygame import KEYDOWN, K_SPACE, event, USEREVENT, mouse
from typing import Dict, Optional, Any, Tuple
from .text_canvas import text_canvas

class GameOver(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                font_path: str,
                position: Optional[Vector2] = None, 
                dimensions: Tuple[int, int] = (5, 5),
                background_color: Color = Color('white'),
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
        self.group: sprite.Group = groups
        self.dimensions = dimensions
        self.background_color = background_color
        self.position: Vector2 = position or Vector2(0, 0)
        
        self.canvas = sprite.Group()
        self.go_text = text_canvas(
            groups= self.canvas,
            font_path= font_path,
            font_size= 25,
            position= Vector2(dimensions[0]//2, 32),
            text= "GAME OVER",
            anchor= 'center'
        )
        self.score_text = text_canvas(
            groups= self.canvas,
            font_path= font_path,
            font_size= 25,
            position= Vector2(dimensions[0]//2, 128),
            anchor= 'center'
        )
        self.retry = text_canvas(
            groups= self.canvas,
            font_path= font_path,
            font_size= 23,
            position= Vector2(dimensions[0]//2, 256),
            text= "RETRY",
            anchor= 'center'
        )
        self.render( debug)

    def update(self, deltaTime: float):

        # Get mouse position in screen coordinates
        mouse_pos = mouse.get_pos()

        # Convert mouse position to be relative to this GameOver sprite
        # Subtract the GameOver sprite's position to get local coordinates
        local_mouse_x = mouse_pos[0] - self.rect.x
        local_mouse_y = mouse_pos[1] - self.rect.y
        local_mouse_pos = (local_mouse_x, local_mouse_y)

        # Now check collision with the retry button using local coordinates
        if self.retry.rect.collidepoint(local_mouse_pos):
            # self.retry.image.fill(Color('red'))
            self.retry.background_color = Color('red')
            # You can add click detection here too
            if mouse.get_pressed()[0]:  # Left mouse button
                print("RETRY clicked!")
        else:
            self.retry.background_color = self.background_color
            
        self.canvas.update(deltaTime)
        self.render(True)

    def render(
        self,
        _debug_: bool = False,
    ):
        self.image: Surface = Surface(self.dimensions)
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