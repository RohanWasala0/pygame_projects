from pygame import KEYDOWN, K_SPACE, SRCALPHA
from pygame import sprite, Vector2, draw, Color, Surface, Rect, event, font
from typing import Tuple, Optional, Dict, Callable
import math

class text_canvas(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                text: str = "Testing",
                font_path: str = None,
                font_size: int = 10,                
                color: Color = Color('black'),
                ) -> None:
        super().__init__(groups)
        
        self.position = position or Vector2()
        self.initial_position = position or Vector2()
        self.color = color or Color('white')
        self.anchor = anchor
        self.input_chart = {}
        self.text = text

        self.font = font.Font(font_path, font_size) 
        
        self.image: Surface = Surface((1, 1), SRCALPHA)
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

        self.render()
        
        self.time = 0
    
    def handling_input(self, event: event) -> None:
        """
        Handles input events the corresponding action from the input chart.
        Attempt to find for the specific key, ui_element, etc
        If the action exist in the input chart execute the mapped action 
        """
        if event_type_action := self.input_chart.get(event.type):
            action = event_type_action.get(getattr(event, 'key', None)) or \
                     event_type_action.get(getattr(event, 'ui_element', None))
            
            if action:
                try:
                    action()
                except Exception as e:
                    print(f"Error executing the action:{action} with error:{e}")
 
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

        self.image = Surface(self.canvas_size, SRCALPHA)
        self.image.fill(Color(0, 0, 0, 0))

        y_offset = 0
        line_spcaing = self.font.get_height()
        
        for line in self.text.split('\n'):
            text_surf = self.font.render(
                text= line,
                antialias= True,
                color= self.color,
            )
            text_rect = text_surf.get_rect(topleft = (0, y_offset))
            y_offset += line_spcaing
            self.image.blit(text_surf, text_rect)

        # draw.rect(
        #     self.image,
        #     Color('white'),
        #     self.image.get_rect(),
        #     width=1,
        # )

        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

    def calculate_canvas_size(self) -> Tuple[int, int]:
        lines = self.text.split('\n')
        max_width = max((self.font.get_height()* len(line)) for line in lines) if lines else 0
        total_height = len(lines)* self.font.get_height()
        
        return max_width, total_height

    def sinusoidal_motion(self, deltaTime: float, amplitude: int, frequency: float, speed: int) -> None:
        self.time += deltaTime * speed
        sine = amplitude * math.sin(frequency * self.time)
        self.position = Vector2(self.position.x, self.initial_position.y + sine)
        
