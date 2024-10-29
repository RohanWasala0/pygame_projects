import sys
import pygame

WIDTH = 640
HEIGHT = 640

#Colors
BACKGROUND_BLACK = pygame.Color('#181C14')
PARTICLES_BEIGE = pygame.Color('#ECDFCC')

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("WFC")

        #system variables 
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.clock = pygame.time.Clock()
        self.deltaTime = 0
        
        #game variables
        
        #Sprite group

        #game objects

        
    def render(self):
        pass
    
    def eventHandling(self, event: pygame.event):
        pass
    
    def update(self):
        pass
        
    def run(self, GAME_FPS: int):
        while True:
            #Render
            self.render()
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.eventHandling(event)

            self.update()
                
            pygame.display.update()
            self.deltaTime = self.clock.tick(GAME_FPS)/ 1000
            
Template(Screen_DIMENSIONS=(WIDTH, HEIGHT)).run(GAME_FPS=60)