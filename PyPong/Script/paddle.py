from pygame import KEYDOWN, KEYUP, FINGERDOWN
from pygame import sprite, Vector2, event, draw, Color, Surface, Rect, math, display
from typing import Tuple, Optional

class Paddle(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                entity_size: Tuple[int, int] = (0, 0), 
                color: Color = Color('black'),
                input_keys: Tuple[int, int] = None) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.entity_size = entity_size
        self.color = color
        
        self.direction: Vector2 = Vector2()
        self.velocity: Vector2 = Vector2()
        self.speed: int = 400
        
        self.input_chart = {
            KEYDOWN: {
                input_keys[0]: lambda: setattr(self, 'velocity', self.add_velocity((0, -1))),
                input_keys[1]: lambda: setattr(self, 'velocity', self.add_velocity((0, 1))),
            },
            KEYUP: {
                input_keys[0]: lambda: setattr(self, 'velocity', self.add_velocity()),
                input_keys[1]: lambda: setattr(self, 'velocity', self.add_velocity()),
            },
            FINGERDOWN: lambda event: self.goto_finger_position(event.x, event.y),
        }
        
        self.render()
        
    def handling_input(self, event: event) -> None:
        """
        Handles input events the corresponding action from the input chart.
        Attempt to find for the specific key, ui_element, etc
        If the action exist in the input chart execute the mapped action 
        """
        if event_type_action := self.input_chart.get(event.type):
            if isinstance(event_type_action, dict):
                if action := event_type_action.get(getattr(event, 'key', None)):
                    try:
                        action()
                    except Exception as e:
                        print(f"Error executing the action:{action} with error:{e}")
            else:
                try:
                    event_type_action(event)
                except Exception as e:
                    print(f"Error executing the action: {event_type_action} with error: {e}")
    
    def update(self, deltaTime: float):
        self.conditions()

        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        self.rect = self.image.get_rect(center= self.position)

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

        draw.rect(
            surface= self.image,
            color= self.color,
            rect= Rect((0, 0), self.entity_size),
        )

        self.rect = self.image.get_rect(center= self.position)

    def conditions(self):
        self.position.y = math.clamp(self.position.y, self.entity_size[1]//2, display.get_window_size()[1] - (self.entity_size[1]//2))

    def add_velocity(self, direction: Tuple[int, int] = (0, 0)):
        return Vector2(direction) * self.speed
    
    def goto_finger_position(self, finger_position_x: float, finger_position_y: float):
        print(finger_position_x, finger_position_y)    
    
    def reset_position(self) -> None:
        self.position.y = display.get_window_size()[1]//2