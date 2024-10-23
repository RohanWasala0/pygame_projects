from pygame import Vector2, Color, KEYDOWN, KEYUP, K_SPACE, draw, math, Surface, Rect, display
from pygame.sprite import Group
import math as mt

from .Entity import Entity

class Bird(Entity):
    def __init__(self, 
            groups: Group, 
            input_key: list,
            position: Vector2 = math.Vector2(), 
            direction: Vector2 = math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: Color = Color('black')) -> None:
        super().__init__(groups, position, direction, entitySize, color)
        
        self.gravity = 250
        self.time = 0
        
        self.inputChart = {
            KEYDOWN: {
                input_key[0]: lambda: setattr(self.direction, 'y', -1) ,
            },
        }
        
        self.image = Surface(size=self.entitySize).convert_alpha()
        self.image.set_colorkey('black')        
        self.render()

    def update(self, deltaTime: float):
        self.direction.y += deltaTime*2.4
        self.direction.y = math.clamp(self.direction.y, -1, 1)
        self.position.y += self.direction.y * self.gravity * deltaTime
        
        self.clampPosition()
        self.rect.center = self.position
        return super().update()
    
    def render(self):
        draw.rect(self.image, self.color, Rect((0, 0), self.entitySize))
        draw.rect(self.image, Color('white'), Rect((30, 20), (3, 3)))
        
        return super().render()
    
    def clampPosition(self):
        self.position.x = math.clamp(self.position.x, self.entitySize[0], display.get_window_size()[0])
        self.position.y = math.clamp(self.position.y, self.entitySize[1], display.get_window_size()[1])

