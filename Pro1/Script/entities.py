import pygame
import random

class Entity:
    def __init__(self, tag: str, position: list) -> None:
        self.X_coordinate = position[0]
        self.Y_coordinate = position[1]
        
        self.Y_movement_bool = (False, False)
        self.X_movement_bool = (False, False)
        
        self.velocity = [0, 0]
        
        self.Color = (0, 0, 255)
        
        self.InputChart = {}
        
    def handle(self, event: pygame.event):
        if event.type in self.InputChart:
            if event.key in self.InputChart[event.type]:
                self.InputChart[event.type][event.key]()
        
    def update(self, ) -> None:
        movement_X = ((self.X_movement_bool[1] - self.X_movement_bool[0]) * 5) + self.velocity[0]
        movement_Y = ((self.Y_movement_bool[1] - self.Y_movement_bool[0]) * 5) + self.velocity[1]
        
        self.X_coordinate += movement_X
        self.Y_coordinate += movement_Y
        
        #self.velocity[1] = min(5, self.velocity[1] + 0.1)
        
    def render(self, surface) -> None:
        self.entity_rect = pygame.draw.circle(surface, self.Color, (self.X_coordinate, self.Y_coordinate), 20)
        self.collision_box = pygame.Rect(self.X_coordinate, self.Y_coordinate, 21, 21)