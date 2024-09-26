import sys
import pygame

class Game:
    #initialization with dimensions as parametors
    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        #window title
        pygame.display.set_caption("Game")

        
        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()
        
    def run(self, GAME_FPS: int):
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
            self.fps.tick(GAME_FPS)
            
Game(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)