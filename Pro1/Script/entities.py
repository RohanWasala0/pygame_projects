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
        
    def handleInput(self, event: pygame.event) -> None:
        
        if hasattr(event, 'type') and event.type in self.inputChart:
            self.inputChart[event.type][event.key]() if hasattr(event, 'key') and event.key in self.inputChart[event.type] else None
            self.inputChart[event.type][event.ui_element]() if hasattr(event, 'ui_element') and event.ui_element in self.inputChart[event.type] else None
                
    
    def update(self):

        pass
    
    def render(self):
        pygame.draw.circle(self.image, color=(0,3,55), center=tuple(x/2 for x in self.image.get_size()), radius=1)
        pass 