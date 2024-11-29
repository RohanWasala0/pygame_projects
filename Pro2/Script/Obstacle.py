from pygame import Vector2, math, Color, draw, Rect, Surface, mask
from pygame.sprite import Group

from .Entity import Entity

class Obstacle(Entity):
    def __init__(self,             
            groups: Group, 
            position: Vector2 = math.Vector2(), 
            direction: Vector2 = math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: Color = Color('black')) -> None:
        super().__init__(groups, position, direction, entitySize, color)
        
        self.speed = 2
        
        self.image: Surface = Surface(size=self.entitySize).convert_alpha()
        self.image.set_colorkey('black')        
        self.render()
        self.mask = mask.from_surface(self.image)
    
    def update(self, deltaTime: float):
        self.direction = Vector2(-1, 0)
        self.position += self.speed* self.direction
        
        self.rect.center = self.position
        self.positionCheck()
        return super().update()
    
    def render(self):

        #draw.rect(self.image, Color('white'), self.rect, 1)
        # self.rect = Rect((0, 0), (self.entitySize[0]+ 20, self.entitySize[1]))
        # #self.rect.center = self.position

        draw.rect(self.image, self.color, Rect((5, 0), (50, self.image.get_height())))
        draw.rect(self.image, Color('white'), Rect((0, 0), (self.image.get_width(), 5)))
        
        self.rect: Rect = self.image.get_rect(center = self.position)
        return super().render()
    
    def positionCheck(self):
        if self.position.x <= 0:
            self.kill()

    
