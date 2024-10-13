import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, 
                groups: pygame.sprite.Group, 
                tag: str, 
                position: pygame.Vector2 = pygame.math.Vector2(), 
                direction: pygame.Vector2 = pygame.math.Vector2(), 
                entitySize: tuple = (0, 0), 
                color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups)
        
        self.tag = tag
        self.position = position
        self.direction = direction
        self.entitySize = entitySize
        self.color = color
        
        self.inputChart = {}
        
    def handleInput(self, 
                event: pygame.event) -> None:
        
        if event.type in self.inputChart:
            if event.key in self.inputChart[event.type]:
                self.inputChart[event.type][event.key]()
                
    
    def update(self):
        pass
    
    def render(self):
        
        pass