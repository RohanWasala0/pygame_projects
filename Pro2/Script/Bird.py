import pygame

from .Entity import Entity

class Bird(Entity):
    def __init__(self, tag: str, position: list, color: pygame.Color, input_keys: list, clock) -> None:
        super().__init__(tag, position, color)
        self.speed = 5
        self.gravity = 3
        self.velocity = [0, 0]
        self.game_clock = clock

        self.InputChart = {
            pygame.KEYDOWN: {
                input_keys[0]: self.impuls,
            }
        }
    
    def update(self) -> None:
        self.X_coordinate += self.speed * self.velocity[0]
        self.Y_coordinate += self.gravity * self.velocity[1]

        #gravity 
        #self.velocity[1] = min(1, self.velocity[1] + 0.1)
        return super().update()

    def render(self, surface: pygame.Surface) -> None:
        self.collision_box = pygame.Rect((0, 0), (40, 40))
        self.collision_box.center = (self.X_coordinate, self.Y_coordinate)
        pygame.draw.rect(surface, self.Color, self.collision_box)

        return super().render(surface)
    
    def impuls(self):
        print("impulse")
        for i in range(4):
            self.velocity[1] = -3
        self.velocity[1] = 0