import pygame
from pygame.sprite import Group

from .entities import Entity

class Menu(Entity, pygame.sprite.Sprite):
    def __init__(self, 
            groups: Group, 
            tag: str, 
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)
        
        self.image = pygame.Surface(size=self.entitySize).convert_alpha()
        self.image.set_colorkey('black')
        self.render()
        
    def render(self):
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.position)
        return super().render()

        