
from pygame import KEYDOWN, K_SPACE, SRCALPHA
from pygame import sprite, Vector2, draw, Color, Surface, Rect, event, font
from typing import Tuple, Optional, Dict, Callable
import math

class text_canvas(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2], 
                font_size: int = 10,                
                font_path: str = None,
                text: str = "Testing",
                anchor: str = 'topleft',
                color: Color = Color('white'),
                ) -> None:
        super().__init__(groups)
        
        self.text = text
        self.anchor = anchor
        self.color = color or Color('white')
        self.position = position or Vector2()
        self.initial_position = position or Vector2()

        self.font:font.Font = font.Font(font_path, font_size) 
        
        self.image: Surface = Surface((1, 1))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

        self.render()
        
        self.time = 0
    
    def update(self, deltaTime: float):
        setattr(self.rect, self.anchor, self.position)

    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        self.canvas_size = self.calculate_canvas_size()
        
        if self.canvas_size == (0, 0): 
            return

        self.image = Surface(self.canvas_size)
        # self.image.fill(V)

        y_offset = 0
        line_spacing = self.font.get_height()
        
        for line in self.text.split('\n'):
            text_surf = self.font.render(
                text= line,
                antialias= True,
                color= self.color,
            )
            text_rect = text_surf.get_rect(topleft = (0, y_offset))
            y_offset += line_spacing
            self.image.blit(text_surf, text_rect)

        draw.rect(
            self.image,
            Color('white'),
            self.image.get_rect(),
            width=1,
        )

        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

    def calculate_canvas_size(self) -> Tuple[int, int]:
        lines = self.text.split('\n')
        max_width = max((self.font.size(line)[0]) for line in lines) if lines else 0
        total_height = len(lines)* self.font.get_height()
        
        return max_width, total_height

    def sinusoidal_motion(self, deltaTime: float, amplitude: int, frequency: float, speed: int) -> None:
        self.time += deltaTime * speed
        sine = amplitude * math.sin(frequency * self.time)
        self.position = Vector2(self.position.x, self.initial_position.y + sine)
        
