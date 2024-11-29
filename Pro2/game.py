import re
import sys
import pygame
import pygame_gui
from pygame_gui.ui_manager import UIManager
import pygame.freetype as ft
import random

from Script.Bird import Bird
from Script.Obstacle import Obstacle
from Script.Menu import Menu, WindowedMenu

WIDTH: int = 640
HEIGHT: int = 480

# Colors
BLACK = pygame.Color('black')
BACKGROUND_BLACK = pygame.Color('#181C14')
OBSTACLE_BROWN = pygame.Color('#3C3D37')
BIRD_GREY = pygame.Color('#697565')
PARTICLES_BEIGE = pygame.Color('#ECDFCC')

class Template:

    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        #system variables 
        self.font = ft.Font('./Assets/m6x11.ttf', 25)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_active = False
        self.deltaTime = 0
        
        #game variables
        self.gapSize = 150
        self.score = 0
        self.score_list: list[int] = []
        self.is_hit = False
        self.is_visible = False
        self.UIManager = UIManager((WIDTH, HEIGHT))
        
        #Sprite group
        self.birdGroup = pygame.sprite.Group()
        self.obstaclesGroup = pygame.sprite.Group()
        
        #game objects
        self.bird = Bird(groups=self.birdGroup, 
                         input_key=[pygame.K_SPACE], 
                         position=pygame.Vector2(WIDTH//2- 80, HEIGHT//2), 
                         entitySize=(40, 40), 
                         color=BIRD_GREY)

        self.windowedMenu = WindowedMenu(
            self,
            pygame.Vector2(50, 50),
            (WIDTH-100, HEIGHT-100),
            self.UIManager)
        # self.menu = Menu(GameManager= self,
        #                 position= pygame.Vector2(WIDTH//2, HEIGHT//2),
        #                 window_size= pygame.display.get_window_size(),
        #                 size= (WIDTH-50, HEIGHT-50),
        #                 color= pygame.Color('white'))
        
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
                            text=f'({self.score})Score',
                            fgcolor=pygame.Color('white'))
        
        self.birdGroup.draw(self.screen) 
        self.obstaclesGroup.draw(self.screen)

        self.UIManager.draw_ui(self.screen)
        # self.menu.render(self.screen)
    
    def eventHandling(self, event):
        self.bird.handleInput(event)
        # self.menu.handleInput(event)
        self.UIManager.process_events(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not self.is_active:
            self.is_active = True
        
    
    def update(self):
        # self.menu.update(self.deltaTime)
        self.UIManager.update(self.deltaTime)
        self.birdGroup.update(self.deltaTime)
        self.obstaclesGroup.update(self.deltaTime)

        if self.is_active:
            self.bird.gravity = 250
            #Game Logics
            if len(self.obstaclesGroup.sprites()) > 1 and self.obstaclesGroup.sprites()[0].position.x == self.bird.position.x:
                self.score += 1
            
            for c in self.obstaclesGroup.sprites():
                if pygame.sprite.collide_mask(self.birdGroup.sprites()[0], c):
                    self.is_active = False
                    self.is_hit = True  
                    self.windowedMenu.visible = 1
        else: 
            self.bird.gravity = 0
            for x in self.obstaclesGroup.sprites():
                x.speed = 0
        
    def run(self, GAME_FPS: int):
        
        last_time = pygame.time.get_ticks()
        while True:
            #self.clock.tick(GAME_FPS)
            self.deltaTime = self.clock.tick(GAME_FPS)/ 1000

            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                self.eventHandling(event)
            
            
            current_time = pygame.time.get_ticks()
            if current_time - last_time > 4000:
                self.genObstacles() if self.is_active else None
                last_time = current_time
            
            #update
            self.update()

            #Render
            self.render()

            pygame.display.update()

    
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

    def reset(self):
        self.obstaclesGroup.empty()
        self.bird.position = pygame.Vector2(240, 240)
        self.bird.direction.y = 0
        self.score_list.append(self.score)
        self.score = 0
        self.is_hit = False
        print(self.score_list)

            
Template().run(GAME_FPS=60)
