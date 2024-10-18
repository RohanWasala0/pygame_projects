import pygame
from pygame.sprite import Group
from random import uniform, randint

from .entities import Entity

class Paddle(Entity, pygame.sprite.Sprite):
    def __init__(self,
            groups: Group, 
            tag: str, 
            input_keys: list,
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: pygame.Color = pygame.Color('black'),
            computerBool: bool = False) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)

        self.computerBool = computerBool
        self.speed = 5
        self.reactionDelay = uniform(0, 0.3)
        
        self._window_size = pygame.display.get_window_size()
        
        if not self.computerBool:
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
        
    def update(self, ballPosition: pygame.Vector2, ballDirection: pygame.Vector2):
            
        self.position.y = min(max(self.position.y, self.image.get_height() // 2), self._window_size[1] - self.image.get_height() // 2)
        
        if self.computerBool:
            #self.computerPaddle(ballPosition, ballDirection, 3)
            #if ballPosition.x > pygame.display.get_window_size()[0]//2:
            self.unbetable__computerpaddle(ballPosition)

        else:
            self.position += self.direction * self.speed
        self.rect.center = self.position
        return super().update()
    
    def render(self):
        
        self.rect = pygame.Rect((0,0), self.entitySize)
        
        pygame.draw.rect(surface=self.image, color=self.color, rect=self.rect)
        self.rect = self.image.get_rect(center=self.position)
        
        return super().render()

    def unbetable__computerpaddle(self, ballPosition: pygame.Vector2):
        Ppos = pygame.Vector2(pygame.display.get_window_size()[0] - 40, 
                              self.position.y)
        Bpos = pygame.Vector2(pygame.display.get_window_size()[0] - 40,      
                              ballPosition.y)
        self.position = Ppos.slerp(Bpos, 0.09)
        
    def computerPaddle(self, ballPosition: pygame.Vector2, ballDirection: pygame.Vector2, difficulty = 0):
        #predicte the ball's y rather than manually assign it 
        predicte_ballY = ballPosition.y + ballDirection.y* self.speed
        
        #random offset and reaction delay based on difficulty
        offset = uniform(-difficulty, difficulty)
        
        #target position for the paddle with offset
        targetY = predicte_ballY
        distanceTo_target = targetY- self.position.y
        # Does not work smoothly #lerp(linear interpolation) the paddle Y coord towards the targetY 
        # self.position.y = pygame.math.lerp(targetY, self.position.y, reactionDelay)
        
        if distanceTo_target > self.reactionDelay:
            directiony = 1
        elif distanceTo_target < -self.reactionDelay:
            directiony = -1
        else:
            directiony = 0
        
        self.direction.y = pygame.math.lerp(self.direction.y, directiony, randint(0, 10)/ 10)
            
        

        
