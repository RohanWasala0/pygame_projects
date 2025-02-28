from pygame import sprite, Vector2, draw, Color, Surface, Rect
from typing import Tuple, Optional
from pygame import freetype 
import math

class text_canvas(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                text: str = "Testing",
                font_path: str = None,
                font_size: int = 10,                
                color: Color = Color('black'),
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.color = color
        self.font = freetype.Font(font_path, font_size)
        self.time = 0
        
        self.text = text
        self.canvas_size = (font_size*len(text), font_size)
        self.initial_position = position or Vector2()
        
        self.render()
    
    def update(self, deltaTime: float):
        self.rect = self.image.get_rect(center= self.position)

    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        if self.canvas_size != (0, 0):
            self.image = Surface(self.canvas_size).convert_alpha()
            self.image.set_colorkey(Color('black'))
            self.image.fill(Color('black'))

        self.font.render_to(
            surf= self.image,
            dest= Rect((0, 0), self.canvas_size),
            text= self.text,
            fgcolor= self.color,
        )

        self.rect = self.image.get_rect(center= self.position)

    def sinusoidal_motion(self, deltaTime: float, amplitude: int, frequency: float, speed: int) -> None:
        self.time += deltaTime * speed
        sine = amplitude * math.sin(frequency * self.time)
        self.position = Vector2(self.position.x, self.initial_position.y + sine)

        
        self.rect = self.image.get_rect(center= self.position)
