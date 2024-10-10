import pygame

from .entities import Entity

class Paddle(Entity):
    def __init__(self, tag: str, position: list, color: tuple, input_keys: list) -> None:
        super().__init__(tag, position, color)
        
        self.Y_movement_bool = (False, False)
        self.X_movement_bool = (False, False)
        
        self.velocity = [0, 0]
        self.speed = 5 
        
        self.InputChart = {
            pygame.KEYDOWN: {
                input_keys[0] : lambda: setattr(self, "Y_movement_bool", (True, self.Y_movement_bool[1])),
                input_keys[1] : lambda: setattr(self, "Y_movement_bool", (self.Y_movement_bool[0], True)),
                },
            pygame.KEYUP: {
                input_keys[0] : lambda: setattr(self, "Y_movement_bool", (False, self.Y_movement_bool[1])),
                input_keys[1] : lambda: setattr(self, "Y_movement_bool", (self.Y_movement_bool[0], False)),
                },
        }
    
    def update(self) -> None:
        self.velocity[0] = self.X_movement_bool[1] - self.X_movement_bool[0]
        self.velocity[1] = self.Y_movement_bool[1] - self.Y_movement_bool[0]
        
        self.X_coordinate += self.speed * self.velocity[0]
        self.Y_coordinate += self.speed * self.velocity[1]
        
        return super().update()
    
    def render(self, surface) -> None:
        self.collision_box = pygame.Rect((0,0), (40, 150))
        self.collision_box.center = (self.X_coordinate, self.Y_coordinate)
        pygame.draw.rect(surface, self.Color, self.collision_box)
        return super().render(surface)
    
