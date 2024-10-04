import pygame

class Entity:
    def __init__(self, tag: str, position: list) -> None:
        self.X_coordinate = position[0]
        self.Y_coordinate = position[1]
        
        self.Color = (0, 0, 255)
        
        self.InputChart = {}
        
    def handle(self, event: pygame.event):
        if event.type in self.InputChart:
            if event.key in self.InputChart[event.type]:
                self.InputChart[event.type][event.key]()
        
    def update(self, ) -> None:
        
        pass
        #self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
    def render(self, surface: pygame.Surface) -> None:
        
        pygame.draw.circle(surface, (0,0,0), (self.X_coordinate, self.Y_coordinate), 1)
        