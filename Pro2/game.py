import sys
import pygame
import pygame.freetype as ft 
import random

from Script.Bird import Bird
from Script.Obstacle import Obstacle

WIDTH = 640
HEIGHT = 480

#Colors
BLACK = pygame.Color('black')
BACKGROUND_BLACK = pygame.Color('#181C14')
OBSTACLE_BROWN = pygame.Color('#3C3D37')
BIRD_GREY = pygame.Color('#697565')
PARTICLES_BEIGE = pygame.Color('#ECDFCC')

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        #system variables 
        self.font = ft.Font('.\Assets\m6x11.ttf', 25)
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.clock = pygame.time.Clock()
        self.active = False
        self.deltaTime = 0
        
        #game variables
        self.gapSize = 150
        self.score = 0
        
        #Sprite group
        self.birdGroup = pygame.sprite.Group()
        self.obstaclesGroup = pygame.sprite.Group()

        #game objects
        self.bird = Bird(groups=self.birdGroup, 
                         input_key=[pygame.K_SPACE], 
                         position=pygame.Vector2(WIDTH//2- 80, HEIGHT//2), 
                         entitySize=(40, 40), 
                         color=BIRD_GREY)
        
        self.genObstacles()
        #self.obstacle.direction.x = -1
        
    def render(self):
        self.screen.fill(BACKGROUND_BLACK)
        pygame.draw.line(self.screen, BLACK, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
        pygame.draw.line(self.screen, BLACK, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
        
        self.font.render_to(surf=self.screen, 
                            dest=pygame.Rect((WIDTH-100, 30), (100, 30)), 
                            text=f'({round(self.clock.get_fps(), 2)})fps',
                            fgcolor=pygame.Color('white'))
        self.font.render_to(surf=self.screen, 
                            dest=pygame.Rect((WIDTH-100, 70), (100, 30)), 
                            text=f'({self.score})Scoure',
                            fgcolor=pygame.Color('white'))
        
        self.birdGroup.draw(self.screen) 
        self.obstaclesGroup.draw(self.screen)
    
    def eventHandling(self, event: pygame.event):
        self.bird.handleInput(event)
        pass
    
    def update(self):

        self.birdGroup.update(self.deltaTime)
        self.obstaclesGroup.update(self.deltaTime)
        
        if self.obstaclesGroup.sprites()[0].position.x == self.bird.position.x:
            self.score += 1
        
    def run(self, GAME_FPS: int):
        
        last_time = pygame.time.get_ticks()
        while True:
            #Render
            self.render()
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.eventHandling(event)
            
            
            current_time = pygame.time.get_ticks()
            if current_time - last_time > 4000:
                self.genObstacles()
                last_time = current_time
            
            # if pygame.sprite.spritecollide(self.bird, self.obstaclesGroup, False):
            #     print("djdjdjjdjdj")  
            #update
            self.update()
                
            pygame.display.update()
            #self.clock.tick(GAME_FPS)
            self.deltaTime = self.clock.tick(GAME_FPS)/ 1000
    
    def genObstacles(self):
        x = random.randint(100, 240)
        y = HEIGHT - self.gapSize - x

        ob = Obstacle(groups=self.obstaclesGroup, 
                 position=pygame.Vector2(WIDTH + 60, x//2), 
                 entitySize=(60, x), 
                 color=OBSTACLE_BROWN)
        ob.image = pygame.transform.flip(ob.image, False, True)


        Obstacle(groups=self.obstaclesGroup, 
                 position=pygame.Vector2(WIDTH + 60, (HEIGHT- y//2)), 
                 entitySize=(60, y), 
                 color=OBSTACLE_BROWN)
            
Template(Screen_DIMENSIONS=(WIDTH, HEIGHT)).run(GAME_FPS=60)