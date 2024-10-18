import pygame
import random, math

from pygame.sprite import Group

from .entities import Entity

class Ball(Entity, pygame.sprite.Sprite):
    def __init__(self, 
            groups: Group, 
            tag: str, 
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: int = 0, 
            color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)

        self.hit = pygame.mixer.Sound('./Assets/hitHurt.wav')
        self.speed = 5
        self.radius = self.entitySize 
        self.lastTime = 0
        
        self.inputChart = {
            pygame.KEYDOWN: {
                pygame.K_SPACE: lambda: setattr(self, 'direction', pygame.math.Vector2(random.choice([1, -1]), 0)),
            }
        }
        
        self.image = pygame.Surface((self.entitySize *2, self.entitySize *2)).convert_alpha()
        self.image.set_colorkey("black")
        self.render()
    
    def update(self):        
        # Handle boundary conditions for Y-axis
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= pygame.display.get_window_size()[1]:
            self.hit.play()
            self.direction.y *= -1
        
        self.position += self.direction * self.speed        
        self.rect.center = self.position
        return super().update()
    
    def render(self):
        pygame.draw.circle(surface=self.image, color=self.color, center=(self.radius, self.radius), radius=self.radius)
        self.rect = self.image.get_rect(center=self.position)
        return super().render()
    
    def reset(self):
        self.direction = pygame.math.Vector2()
        self.position = pygame.math.Vector2(tuple(x/2 for x in pygame.display.get_window_size()))

        
    def change_angle(self, angles) -> None:
        angle = random.uniform(math.radians(angles[0]), math.radians(angles[1]))
        self.direction = pygame.math.Vector2(math.cos(angle), math.sin(angle)).normalize()
        




