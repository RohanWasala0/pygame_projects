import pygame
import random
from pygame.sprite import Group

from .entities import Entity

class Particles(Entity, pygame.sprite.Sprite):
    def __init__(self,
            groups: Group, 
            tag: str, 
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: int = 0, 
            color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)

        self.radius = self.entitySize
        self.speed = random.randint(5, 20)
        self.alpha = 225
        self.fadeSpeed = 15
        
        self.image = pygame.Surface((self.entitySize *2, self.entitySize *2)).convert_alpha()
        self.image.set_colorkey('black')
        self.render()
    
    def update(self):
        self.position += self.direction * self.speed
        
        self.rect.center = self.position
        self.check_position()
        self.fade_alpha()
        return super().update()
    
    def render(self):
        pygame.draw.circle(surface=self.image, color=self.color, center=(self.radius, self.radius), radius=self.radius)
        self.rect = self.image.get_rect(center=self.position)
        #return super().render()
    
    def check_position(self):
        if (
            self.position.x < -50 or
            self.position.x > pygame.display.get_window_size()[0] + 50 or
            self.position.y < -50 or 
            self.position.y > pygame.display.get_window_size()[1] + 50 
        ):
            self.kill()
        
    def fade_alpha(self):
        #print(int(100 * tick_delta))
        self.alpha -= self.fadeSpeed
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)
        
