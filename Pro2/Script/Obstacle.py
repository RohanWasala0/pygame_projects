import pygame

from .Entity import Entity

class Obstacle(Entity):
    def __init__(self, tag: str, position: list, color: pygame.Color, Obstacle_size: tuple) -> None:
        super().__init__(tag, position, color)
        self.size = Obstacle_size
        self.speed = 2
        
    def render(self, surface: pygame.Surface) -> None:
        self.Obstacle_rect = pygame.Rect((self.X_coordinate, self.Y_coordinate), self.size)
        pygame.draw.rect(surface, self.Color, self.Obstacle_rect)
        return super().render(surface)
    
    def update(self) -> None:
        self.X_coordinate += self.speed * self.velocity[0]
        # if self.active:
        #     self.velocity[0] = min(1, self.velocity[0] + 0.1)
        self.velocity[0] = min(-1, self.velocity[0] + 0.1)
        return super().update()