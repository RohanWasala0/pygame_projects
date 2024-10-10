import pygame

from .entities import Entity

class Menu(Entity):
    def __init__(self, tag: str, position: list, color: tuple) -> None:
        super().__init__(tag, position, color)
        
    def render(self, surface, menuSize: tuple) -> None:
        menuSurface = pygame.Surface(menuSize, pygame.SRCALPHA)
        menuSurface.fill(self.Color)
        surface.blit(menuSurface, (self.X_coordinate , self.Y_coordinate ))
        
        return super().render(surface)
        