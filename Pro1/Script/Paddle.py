import pygame
from pygame.sprite import Group

from .entities import Entity

class Paddle(Entity, pygame.sprite.Sprite):
    def __init__(self, 
            groups: Group, 
            tag: str, 
            input_keys: list,
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)

        self.speed = 5
        
        self.inputChart = {
            pygame.KEYDOWN: {
                input_keys[0] : lambda: setattr(self, "direction", pygame.Vector2(0, -1)),
                input_keys[1] : lambda: setattr(self, "direction", pygame.Vector2(0, 1)),
                },
            pygame.KEYUP: {
                input_keys[0] : lambda: setattr(self, "direction", pygame.Vector2(0, 0)),
                input_keys[1] : lambda: setattr(self, "direction", pygame.Vector2(0, 0)),
                },
        }
        
        self.image = pygame.Surface(size=self.entitySize).convert_alpha()
        self.image.set_colorkey('black')
        self.render()
        
    def update(self):
        self.position += self.direction * self.speed
        
        self.rect.center = self.position
        return super().update()
    
    def render(self):
        
        self.rect = pygame.Rect((0,0), self.entitySize)
        
        pygame.draw.rect(surface=self.image, color=self.color, rect=self.rect)
        self.rect = self.image.get_rect(center=self.position)
        
        return super().render()


    
