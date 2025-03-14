import sys
import asyncio
import pygame

from utils import *
from script.bird import Bird

class PyBird():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("PyBird")
        
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.SRCALPHA)

        self.bird_group = pygame.sprite.Group()
        self.bird = Bird(
            groups= self.bird_group,
            position= pygame.Vector2(WIDTH//2, HEIGHT//2),
            anchor= 'center',
            sheet= BIRD_SHEET,
        )

    def render(self) -> None:
        self.screen.fill(BACKGROUND_BLACK)

        self.bird_group.draw(self.screen)
        
    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
    def update(self, deltaTime: float) -> None:
        pass

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
