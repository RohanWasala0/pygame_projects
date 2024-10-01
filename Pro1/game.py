import sys
import pygame

from Script.entities import Entity

class Template:

    def __init__(self, Screen_DIMENSIONS: list) -> None:
        pygame.init()
        pygame.display.set_caption("Game")

        self.screen = pygame.display.set_mode((Screen_DIMENSIONS[0], Screen_DIMENSIONS[1]))
        self.fps = pygame.time.Clock()

        self.collision_area = pygame.Rect(50, 50, 300, 50)
        self.player = Entity('player', (320, 240))
    def run(self, GAME_FPS: int):
        while True:
            self.fps.tick(GAME_FPS)
            #Render
            self.screen.fill((0, 0, 0))
            self.player.render(self.screen)
            
            #Handle Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.player.handle(event)

            #Update 
            self.player.update()
            
            if self.player.collision_box.colliderect(self.collision_area):
                print("collided")
                pygame.draw.rect(self.screen, (0, 100, 255), self.collision_area)
            else:
                #print("collided")
                pygame.draw.rect(self.screen, (0, 50, 155), self.collision_area)
                
            pygame.display.update()
            
            
            
Template(Screen_DIMENSIONS=(640, 480)).run(GAME_FPS=60)