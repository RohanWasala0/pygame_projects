from pygame import sprite, Vector2, event, draw, Color, Surface
from typing import Tuple, Optional

class Entity(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                direction: Optional[Vector2] = None, 
                entity_size: Tuple[int, int] = (0, 0), 
                color: Color = Color('black')) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.direction = direction or Vector2()
        self.entity_size = entity_size
        self.color = color
        
        self.input_chart = {}
        
        self.render()
        
    def handleInput(self, event: event) -> None:
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

        pass
    
    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        if self.entity_size != (0, 0):
            self.image = Surface(self.entity_size).convert_alpha()
            self.image.set_colorkey(Color('black'))
            self.image.fill(Color('black'))

        self.rect = self.image.get_rect(center= self.position)
