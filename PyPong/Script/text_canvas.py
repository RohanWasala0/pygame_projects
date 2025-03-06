from pygame import sprite, Vector2, draw, Color, Surface, Rect, event, KEYDOWN, K_SPACE
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
        self.canvas_size = []
        self.initial_position = position or Vector2()
        
        self.input_chart = {
            KEYDOWN: {
                K_SPACE: self.kill,
            },
        }

        self.render()
    
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
        self.rect = self.image.get_rect(topleft= self.position)

    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        lines = self.text.split('\n')
        self.canvas_size = [(max(len(s) for s in lines))*self.font.get_sized_height(), len(lines)*self.font.get_sized_height()]

        #print(self.canvas_size)
        
        if self.canvas_size != (0, 0):
            self.image = Surface(self.canvas_size).convert_alpha()
            self.image.set_colorkey(Color('black'))
            self.image.fill(Color('black'))

        y_offset = 0
        line_spcaing = self.font.get_sized_height()
        
        for line in lines:
            self.font.render_to(
                surf= self.image,
                dest= Rect((0, y_offset), self.canvas_size),
                text= line,
                fgcolor= self.color,
            )
            y_offset += line_spcaing

        draw.rect(
            self.image,
            Color('white'),
            self.image.get_rect(),
            width=1,
        )

        self.rect = self.image.get_rect(topleft = self.position)

    def sinusoidal_motion(self, deltaTime: float, amplitude: int, frequency: float, speed: int) -> None:
        self.time += deltaTime * speed
        sine = amplitude * math.sin(frequency * self.time)
        self.position = Vector2(self.position.x, self.initial_position.y + sine)

        
        self.rect = self.image.get_rect(center= self.position)
