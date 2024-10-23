from pygame import sprite, Vector2, event, draw, Color

class Entity(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Vector2 = Vector2(), 
                direction: Vector2 = Vector2(), 
                entitySize: tuple = (0, 0), 
                color: Color = Color('black')) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position
        self.direction = direction
        self.entitySize = entitySize
        self.color = color
        
        self.inputChart = {}
        
        
    def handleInput(self, event: event) -> None:
        
        if hasattr(event, 'type') and event.type in self.inputChart:
            self.inputChart[event.type][event.key]() if hasattr(event, 'key') and event.key in self.inputChart[event.type] else None
            self.inputChart[event.type][event.ui_element]() if hasattr(event, 'ui_element') and event.ui_element in self.inputChart[event.type] else None
                
    
    def update(self):

        pass
    
    def render(self):
        draw.circle(self.image, color=(0,3,55), center=tuple(x/2 for x in self.image.get_size()), radius=1)
        self.rect = self.image.get_rect(center=self.position)
        pass 