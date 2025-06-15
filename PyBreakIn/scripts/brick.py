from pygame import sprite, Vector2, event, draw, Color, Surface, Rect, math, display, mask, SRCALPHA
from typing import Tuple, Optional
from input_manager import InputManager

class Bricks(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                anchor: str = 'topleft',
                color: Color = Color('black'),
                position: Optional[Vector2] = None, 
                dimensions: Tuple[int, int] = (0, 0),
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.color: Color = color
        self.anchor: str = anchor
        self.dimensions: Tuple[int, int] = dimensions
        self.position: Vector2 = position or Vector2()
        
        self.direction: Vector2 = Vector2()
        self.velocity: Vector2 = Vector2()
        self.speed: int = 400

        self.render()
    
    def update(self, deltaTime: float):

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
        self.image.fill(Color('black'))
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
