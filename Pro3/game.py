import pygame
import pygame_gui
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
        self.UIManager = pygame_gui.UIManager((WIDTH, HEIGHT))
        
        #game variables
        self.noBirds = 100
        self.changeWeights = False
        
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
            
        #Render UI for weight
        self.renderMenu()
        
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
        
        self.entityGroup.draw(self.screen)
        self.UIManager.draw_ui(self.screen)

          
    def eventHandling(self, event: pygame.event):
        for x in self.entityGroup.sprites():
            x.handleInput(event)
            
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element in self.weightChart:
                self.weights[self.weightChart[event.ui_element]['value']] = event.value
                self.changeWeights = True
        if event.type == pygame.MOUSEBUTTONUP and self.changeWeights:
            for y in self.entityGroup.sprites():
                y.weights = self.weights
            self.changeWeights = False
  


    
    def update(self):
        self.entityGroup.update(self.deltaTime, targetPos=pygame.Vector2(pygame.mouse.get_pos()))

        self.UIManager.update(self.deltaTime)
        pygame.display.update()

        
    def run(self):
        while True:
            self.deltaTime = self.clock.tick(GAME_FPS)/ 1000
            #Render
            self.render()
            
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.UIManager.process_events(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.print_debug_info()
                self.eventHandling(event)
            
            #Update
            self.update()
            
    def renderMenu(self):
        
        self.separation_weight_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((0, HEIGHT - 70), ((WIDTH//3), 30)),
            start_value=1.5,
            value_range=[0, 5],
            manager=self.UIManager,
            click_increment=0.5,
        )
        self.separation_weight_slider_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((0, HEIGHT - 100), ((WIDTH//3), 30)),
            text='Separation weight',
            manager=self.UIManager,   
        )
        
        self.alignment_weight_silder = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(((WIDTH//3), HEIGHT - 70), ((WIDTH//3), 30)),
            start_value=1.0,
            value_range=[0, 5],
            manager=self.UIManager,
            click_increment=0.5,
        )
        self.alignment_weight_silder_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(((WIDTH//3), HEIGHT - 100), ((WIDTH//3), 30)),
            text='Alignment weight',
            manager=self.UIManager, 
        )
        
        self.cohesion_weight_silder = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH-(WIDTH//3), HEIGHT - 70), ((WIDTH//3), 30)),
            start_value=1.0,
            value_range=[0, 5],
            manager=self.UIManager,
            click_increment=0.5,
        )
        self.cohesion_weight_silder_lable = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH-(WIDTH//3), HEIGHT - 100), ((WIDTH//3), 30)),
            text='Cohesion weight',
            manager=self.UIManager,
        )
        
        self.weightChart = {
            self.separation_weight_slider:{ 'value': 0},
            self.alignment_weight_silder:{ 'value': 1},
            self.cohesion_weight_silder:{ 'value': 2},
        }
        self.weights = [1.5, 1.0, 1.0]
        
            
Game(Screen_DIMENSIONS=[WIDTH, HEIGHT]).run()