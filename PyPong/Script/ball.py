from math import radians, sin, cos
from random import uniform
from pygame import sprite, Vector2, event, draw, Color, Surface, KEYDOWN, K_SPACE, display
from typing import Tuple, Optional

class Ball(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                entity_size: Tuple[int, int] = (0, 0), 
                color: Color = Color('black')) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.entity_size = entity_size
        self.color = color
        
        self.velocity = Vector2()
        self.radius = self.entity_size[0]//2
        self.speed = 600
        self.start = True

        self.input_chart = {
            KEYDOWN: {
                K_SPACE: lambda: setattr(self, 'velocity', self.rand_velocity()),
            }
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
    
    def update(self, deltaTime: float) -> None:
        self.conditions()

        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        self.rect.center = self.position

    def render(self) -> None:
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        if self.entity_size != (0, 0):
            self.image = Surface(self.entity_size).convert_alpha()
            self.image.set_colorkey(Color('black'))
            self.image.fill(Color('black'))

        draw.circle(
            surface= self.image,
            color= self.color,
            center= (self.radius, self.radius),
            radius= self.radius,

        )

        self.rect = self.image.get_rect(center= self.position)

    def conditions(self) -> None:
        if self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity = self.velocity.reflect(Vector2(0, 1))
        elif self.position.y > display.get_window_size()[1] - self.radius:
            self.position.y = display.get_window_size()[1] - self.radius
            self.velocity = self.velocity.reflect(Vector2(0, 1))


    def rand_velocity(self) -> Vector2:
        print("running")
        while True:
            direction = Vector2(uniform(-1, 1), uniform(-1, 1))
            return direction.normalize() * self.speed
    
    def change_angle(self, angles: Tuple[int, int]) -> Vector2:
        angle = uniform(radians(angles[0]), radians(angles[1]))
        return Vector2(cos(angle), sin(angle)).normalize() * self.speed

    def reset_position(self) -> None:
        self.velocity = Vector2()
        self.rect = self.rect.move_to(center= Vector2(tuple(x/2 for x in display.get_window_size())))
        self.position = Vector2(self.rect.center)
