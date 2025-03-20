import sys
import asyncio
import pygame

from utils import *
from script.bird import Bird
from script.environment import Environment

class PyBird():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyBird")
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)
        self._grid_background()

        self.bird_group = pygame.sprite.Group()
        self.bird = Bird(
            groups= self.bird_group,
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            anchor= 'center',
            sheet= BIRD_SHEET,
        )

        self.environment_sheet = pygame.sprite.Group()
        self.env_sheet = Environment(
            groups= self.environment_sheet,
            position = pygame.Vector2( WIDTH//4, HEIGHT//4),
            anchor= 'center',
            BACKGROUND_AIR= BACKGROUND_AIR,
        )

    def _grid_background(self) -> None:
        self.background = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)

        for x in range(0, WIDTH, 40):
            pygame.draw.line(self.background, pygame.Color(173, 170, 170, 75), (x, 0), (x, HEIGHT)) 
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(self.background, pygame.Color(173, 170, 170, 75), (0, y), (WIDTH, y)) 
    
    def render(self) -> None:
        self.screen.fill(BACKGROUND_BLACK)
        self.screen.blit(self.background)

        self.environment_sheet.draw(self.screen)
        self.bird_group.draw(self.screen)
        self.bird.render()
        
        # for i, tile in enumerate(self.env_sheet.animation_list):
        #     scaled = pygame.transform.scale(tile, (40, 40))
        #     self.screen.blit(scaled, ((i%16)* 40, (i//16)* 40))
        
    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    def update(self, deltaTime: float) -> None:
        self.bird_group.update(deltaTime)

async def main() -> None:
    deltaTime: float = 0.0
    clock = pygame.time.Clock()
    game = PyBird()
    while True:
        game.render()
        game.handle_input()
        game.update(deltaTime)

        deltaTime = clock.tick(60) / 1000
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
