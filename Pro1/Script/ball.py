import pygame
import random, math

from .entities import Entity

class Ball(Entity):
    def __init__(self, tag: str, position: list, color: pygame.color) -> None:
        super().__init__(tag, position, color)
        
        self.radius = 20
        self.speed = 5
        self.velocity = [0, 0]
        
        self.InputChart = {
            pygame.KEYDOWN: {
                pygame.K_SPACE : lambda: setattr(self, 'velocity', [int(random.choice([1, -1])), 0]),
            } 
        }
        
    def update(self) -> None:
        # Update ball's position based on current velocity
        self.X_coordinate += self.speed * self.velocity[0]
        self.Y_coordinate += self.speed * self.velocity[1]
        
        # Handle boundary conditions for X-axis
        # if self.X_coordinate <= 0 or self.X_coordinate >= 640:
        #     self.velocity[0] *= -1
        #     #self.X_coordinate = max(self.radius, min(640 - self.radius - 1, self.X_coordinate))  # Keep ball within screen
        
        # Handle boundary conditions for Y-axis
        if self.Y_coordinate <=0 or self.Y_coordinate >= 480:
            self.velocity[1] *= -1
        
        return super().update()
    
    def render(self, surface: pygame.Surface) -> None:
        self.collision_box = pygame.Rect((self.X_coordinate - 20, self.Y_coordinate - 20), (40, 40))
        pygame.draw.rect(surface, (0,255, 0), self.collision_box)
        
        pygame.draw.circle(surface, self.Color, (self.X_coordinate, self.Y_coordinate), 20)
        return super().render(surface)
    
    def change_angle(self, angles):
        #Change the ball's direction to a random angle on collision with a paddle 
        angle = random.uniform(math.radians(angles[0]), math.radians(angles[1]))
        self.velocity[0] = math.cos(angle) 
        self.velocity[1] = math.sin(angle)