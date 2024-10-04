import pygame

from .entities import Entity

class Ball(Entity):
    def __init__(self, tag: str, position: list, ) -> None:
        super().__init__(tag, position)
        
        self.Y_movement_bool = (False, False)
        self.X_movement_bool = (False, False)
        
        self.velocity = [0, 0]
        
        self.InputChart = {
            pygame.KEYDOWN: {
                #pygame.K_g : lambda: setattr(self, 'velocity', min(5, self.velocity[0] + 0.1)),
                pygame.K_SPACE : lambda: setattr(self, 'velocity', [5, 0]),
            } 
        }
        
    def update(self) -> None:
        movement_X = ((self.X_movement_bool[1] - self.X_movement_bool[0]) * 5) + self.velocity[0]
        movement_Y = ((self.Y_movement_bool[1] - self.Y_movement_bool[0]) * 5) + self.velocity[1]
        
        self.X_coordinate += movement_X
        self.Y_coordinate += movement_Y
        
        if self.X_coordinate < 0 or self.X_coordinate > 640:
            self.velocity[0] = 0
            self.X_coordinate = 320
        return super().update()
    
    def render(self, surface: pygame.Surface) -> None:
        self.collision_box = pygame.Rect((self.X_coordinate - 20, self.Y_coordinate - 20), (40, 40))
        pygame.draw.rect(surface, (0,255, 0), self.collision_box)
        
        pygame.draw.circle(surface, self.Color, (self.X_coordinate, self.Y_coordinate), 20)
        return super().render(surface)