import pygame
import pygame.freetype as ft
import sys
from random import randint, uniform

from entity import Entity

GAME_FPS = 60
WIDTH, HEIGHT = 1280, 720

class Game:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        #system variables 
        self.font = ft.Font('.\m6x11.ttf',20)
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.clock = pygame.time.Clock()
        self.deltaTime = 0
        
        #game variables
        self.noBirds = 100
        
        #Sprite group
        self.entityGroup = pygame.sprite.Group()

        #game objects
        for x in range(self.noBirds):
            randDir = pygame.Vector2(uniform(-1, 1), uniform(-1, 1))
            Entity(tag=f"bird{x}",
                   groups=self.entityGroup, 
                   position=pygame.Vector2(randint(100, WIDTH-100), randint(100, HEIGHT-100)),
                   direction=randDir.normalize(),
                   entitySize=(20, 20),
                   color=pygame.Color('white'))
        
        # self.en = Entity(groups=self.entityGroup, 
        #        position=pygame.Vector2(WIDTH//2, HEIGHT//2),
        #        entitySize=(40, 40),
        #        color=pygame.Color('white'))
        # print(list(vars(x) for x in self.entityGroup.sprites()))
        
    def render(self):
        self.screen.fill(pygame.Color('black'))
        self.font.render_to(surf=self.screen, 
                            dest=pygame.Rect((WIDTH-100, 30), (100, 30)), 
                            text=f'({round(self.clock.get_fps(), 2)})fps',
                            fgcolor=pygame.Color('white'))
        
        self.font.render_to(surf=self.screen, 
                            dest=pygame.Rect((WIDTH-100, 70), (100, 30)), 
                            text=f'({self.noBirds})Birds',
                            fgcolor=pygame.Color('white'))
        
        self.font.render_to(surf=self.screen, 
                            dest=pygame.Rect((0, HEIGHT - 30), (WIDTH, 30)), 
                            text='Press the left mouse button and move around to seek the birds towards the mouse',
                            fgcolor=pygame.Color('white'))
        
        # self.drawLine_centerMass()
        self.entityGroup.draw(self.screen)
        
        # center_mass = pygame.Vector2()
        # for x in self.entityGroup.sprites():
        #     center_mass += x.position
        # center_mass /= len(self.entityGroup.sprites())
        # for x in self.entityGroup.sprites():
        #     pygame.draw.line(self.screen, pygame.Color('white'), x.position, center_mass)

          
    def eventHandling(self, event: pygame.event):
        for x in self.entityGroup.sprites():
            x.handleInput(event)

    
    def update(self):
        self.entityGroup.update(self.deltaTime, targetPos=pygame.Vector2(pygame.mouse.get_pos()))

        pygame.display.update()
        self.deltaTime = self.clock.tick(GAME_FPS)/ 1000
        
    def run(self):
        while True:
            #Render
            self.render()
            
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.eventHandling(event)
            
            #Update
            self.update()
            
    def drawLine_centerMass(self):
        centerMass = pygame.Vector2()
        for x in self.entityGroup.sprites():
            centerMass += x.position
        centerMass /= len(self.entityGroup.sprites())
        for x in self.entityGroup.sprites():
            pygame.draw.line(self.screen, pygame.Color('white'), x.position, centerMass)
            
Game(Screen_DIMENSIONS=[WIDTH, HEIGHT]).run()