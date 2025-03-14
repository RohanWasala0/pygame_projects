from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA
from typing import Tuple, Optional

class Bird(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                sheet: Surface = Surface((0, 0)), 
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.anchor = anchor
        self.sheet = sheet
        
        self.input_chart = {}
        
        self.image: Surface = Surface((16, 16), SRCALPHA)
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
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
    
    def update(self):
        setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        self.image = Surface((16, 16), SRCALPHA)
        self.image.fill(Color(0, 0, 0, 0))
        self.image.blit(self.sheet, ((0, 0), (16, 16)))

        self.image.convert_alpha()
        setattr(self.rect, self.anchor, self.position)