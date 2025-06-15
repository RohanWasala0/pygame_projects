from pygame import KEYDOWN, KEYUP, FINGERDOWN, SRCALPHA, K_a, K_d, K_LEFT, K_RIGHT
from pygame import sprite, Vector2, event, draw, Color, Surface, Rect, math, display, mask
from typing import Tuple, Optional
from input_manager import InputManager

AXIS_SENSITIVITY = 5.0       # Speed of interpolation
AXIS_GRAVITY = 8.0           # Speed of returning to 0

class Paddle(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                anchor: str = 'topleft',
                color: Color = Color('black'),
                position: Optional[Vector2] = None, 
                dimensions: Tuple[int, int] = (0, 0), 
                input_keys: Tuple[int, int] = None) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.color: Color = color
        self.anchor: str = anchor
        self.dimensions: Tuple[int, int] = dimensions
        self.position: Vector2 = position or Vector2()
        self.input_manager = InputManager()
        
        self.target_direction: Vector2 = Vector2()
        self.direction: Vector2 = Vector2()
        self.velocity: Vector2 = Vector2()
        self.speed: int = 400
        
        self.input_manager.input_chart = {
            'continuous': {
                (K_a, K_LEFT): lambda: setattr(self.target_direction, 'x', -1),
                (K_d, K_RIGHT): lambda: setattr(self.target_direction, 'x', 1),
                'default': lambda: setattr(self, 'target_direction', Vector2()),
            }
        }

        self.render()
    
    def update(self, deltaTime: float):
        self.conditions()
        self.direction = Vector2(self.axis_smoothing(self.direction.x, self.target_direction.x, deltaTime), self.axis_smoothing(self.direction.y, self.target_direction.y, deltaTime))
        self.velocity = self.direction * self.speed
        self.position = self.position + (self.velocity * deltaTime)
        self.render()

    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        if self.dimensions != (0, 0):
            self.image = Surface(self.dimensions, SRCALPHA)
        self.image.set_colorkey(Color('black'))
        # self.image.fill(Color('black'))
        self.image.fill(self.color)

        self.rect = self.image.get_rect()
        draw.rect(
            self.image,
            Color('white'),
            self.image.get_rect(),
            width= 1,
        )

        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        setattr(self.rect, self.anchor, self.position)

    def conditions(self):
        self.position.x = math.clamp(self.position.x, self.dimensions[0]//2, display.get_window_size()[0] - (self.dimensions[0]//2))

    def goto_finger_position(self, finger_position_x: float, finger_position_y: float):
        print(finger_position_x, finger_position_y)    

    def reset(self) -> None:
        self.position.y = display.get_window_size()[1]//2

    def axis_smoothing(self, value, target, dt) -> float:
        # Smooth movement toward target
        if target != 0:
            delta = AXIS_SENSITIVITY * dt
        else:
            delta = AXIS_GRAVITY * dt

        if value < target:
            value = min(value + delta, target)
        elif value > target:
            value = max(value - delta, target)

        return value