import pygame

from .Entity import Entity

class Bird(Entity):
    def __init__(self, tag: str, position: list, color: pygame.Color, input_keys: list) -> None:
        super().__init__(tag, position, color)
        self.gravity = 2

        self.InputChart = {
            pygame.KEYDOWN: {
                input_keys[0]: lambda: setattr(self, 'velocity', [0, -2]),
            }
        }
    
    def update(self) -> None:
        #self.X_coordinate += self.speed * self.velocity[0]
        self.Y_coordinate += (self.gravity * self.velocity[1])

        #gravity 
        if self.active:
            self.velocity[1] = min(1, self.velocity[1] + 0.1)
        return super().update()

    def render(self, surface: pygame.Surface) -> None:
        self.collision_box = pygame.Rect((0, 0), (40, 40))
        self.collision_box.center = (self.X_coordinate, self.Y_coordinate)
        pygame.draw.rect(surface, self.Color, self.collision_box)

        return super().render(surface)
