import sys
import pygame

from Script.Bird import Bird

WIDTH = 640
HEIGHT = 480

#colors
SKI_BLUE = (111, 211, 255)
RED = (255, 0, 0)

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")
        self.clock = 0

        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()

        self.bird = Bird('bird', (WIDTH/2, HEIGHT/4), RED, [pygame.K_SPACE], self.clock)
        
    def run(self, GAME_FPS: int):
        while True:

            #Render
            self.screen.fill(SKI_BLUE)

            self.bird.render(self.screen)
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.bird.handle(event)
            
            #game conditions
                
            #Update 
            self.bird.update()
            self.clock += 1
            pygame.display.update()

            self.fps.tick(GAME_FPS)
            
            
            
Template(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)