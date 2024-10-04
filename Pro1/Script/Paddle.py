import pygame

from .entities import Entity

class Paddle(Entity):
    def __init__(self, tag: str, position: list, input_keys: list) -> None:
        super().__init__(tag, position)
        
        self.Y_movement_bool = (False, False)
        self.X_movement_bool = (False, False)
        
        self.velocity = [0, 0]
        
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
        movement_X = ((self.X_movement_bool[1] - self.X_movement_bool[0]) * 5) + self.velocity[0]
        movement_Y = ((self.Y_movement_bool[1] - self.Y_movement_bool[0]) * 5) + self.velocity[1]
        
        self.X_coordinate += movement_X
        self.Y_coordinate += movement_Y
        
        return super().update()
    
    def render(self, surface: pygame.Surface) -> None:
        self.collision_box = pygame.Rect((self.X_coordinate - 20, self.Y_coordinate - 100), (40, 200))
        pygame.draw.rect(surface, (0,255, 0), self.collision_box)
        # self.entity_rect = pygame.draw.circle(surface, self.Color, (self.X_coordinate, self.Y_coordinate), 20)
        #self.entitySurface.blit(surface, (self.X_coordinate, self.Y_coordinate))
        #self.collision_box = pygame.Rect(self.X_coordinate, self.Y_coordinate, self.entitySurface.get_width(), self.entitySurface.get_height())
        return super().render(surface)
    
