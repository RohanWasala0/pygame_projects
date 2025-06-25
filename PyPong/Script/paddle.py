from pygame import (
        sprite, 
        Vector2, 
        draw, 
        Color, 
        Surface, 
        Rect, 
        math, 
        display, 
        SRCALPHA,
        mask,
        FINGERMOTION,
    ) 
from typing import Tuple, Optional
from input_manager import InputManager

AXIS_SENSITIVITY = 5.0       # Speed of interpolation
AXIS_GRAVITY = 8.0           # Speed of returning to 0

class Paddle(sprite.Sprite):
    def __init__(
        self, 
        groups: sprite.Group,
        keys,
        zone,
        anchor: str = 'topleft',
        color: Color = Color('black'),
        position: Optional[Vector2] = Vector2(), 
        dimensions: Tuple[int, int] = (0, 0), 
    ):
        super().__init__(groups)
        
        self.color = color
        self.group = groups
        self.anchor = anchor
        self.position = position 
        self.dimensions = dimensions
        self.input_manager = InputManager()
        
        self.direction: Vector2 = Vector2()
        self.target_direction: Vector2 = Vector2()
        self.velocity: Vector2 = Vector2()
        self.speed: int = 400
        
        self.input_manager.input_chart = {
            'continuous': {
                keys[0]: lambda: setattr(self.target_direction, 'y', -1),
                keys[1]: lambda: setattr(self.target_direction, 'y', 1),
                'default': lambda: setattr(self, 'target_direction', Vector2()),
            },
            'touch': {
                FINGERMOTION: {
                    zone: lambda event: setattr(self.position, 'y', event.y*display.get_window_size()[1])
                }
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

        self.image = Surface(self.dimensions, SRCALPHA) if self.dimensions != (0, 0) else Surface((5, 5), SRCALPHA)
        self.image.set_colorkey(Color('black'))
        self.image.fill(Color('black'))
        self.image.fill(self.color)

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
        self.position.y = math.clamp(self.position.y, self.dimensions[1]//2, display.get_window_size()[1] - (self.dimensions[1]//2))

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