import sys
import pygame
import random

from Script.Bird import Bird
from Script.Obstacle import Obstacle

WIDTH = 640
HEIGHT = 480

#colors
SKI_BLUE = (111, 211, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        #system variables 
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()
        self.active = False
        
        #game variables
        self.gapSize = 100
        self.genBool = False
        self.genClock = 0

        #game objects
        self.bird = Bird('bird', (WIDTH/2, HEIGHT/2), RED, [pygame.K_SPACE])
        self.bird.active = self.active
        self.renderList_obstacle = []
        self.endLine = pygame.Rect((0,0),(5, 480))
        
        self.genObstacles()
        
    def run(self, GAME_FPS: int):
        last_time = pygame.time.get_ticks()
        while True:
            #Render
            self.screen.fill(SKI_BLUE)
            self.bird.render(self.screen)
            [x.render(self.screen) for x in self.renderList_obstacle]
            pygame.draw.rect(self.screen, RED, self.endLine)
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.active:
                    self.bird.handle(event)
            
            #game conditions
            for x in self.renderList_obstacle:
                if hasattr(x, 'Obstacle_rect'):
                    if x.Obstacle_rect.colliderect(self.endLine) :
                        self.renderList_obstacle.pop(0)
                        self.renderList_obstacle.pop(0)
            
            current_time = pygame.time.get_ticks()
            if current_time - last_time > 2000:
                self.genObstacles()
                last_time = current_time
                
            #Update 
            self.bird.update()
            [x.update() for x in self.renderList_obstacle]
                
            pygame.display.update()
            self.fps.tick(GAME_FPS)
    
    def genObstacles(self):
        x = random.randint(20, 240)
        y = HEIGHT - self.gapSize - x
        #print(f'x={x}, y={y}')
        self.renderList_obstacle.append(Obstacle('obstacle', (WIDTH, 0), GREEN, (50, x)))
        self.renderList_obstacle.append(Obstacle('obstacle', (WIDTH, 150 + x), GREEN, (50, y)))
    

            
            
            
Template(Screen_DIMENSIONS=(WIDTH, HEIGHT)).run(GAME_FPS=60)