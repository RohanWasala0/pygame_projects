import sys
import asyncio
import pygame

class GameName():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("GameName")
        

    def render(self) -> None:
        pass
        
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
    game = GameName()
    while True:
        game.render()
        game.handle_input()
        game.update(deltaTime)

        deltaTime = clock.tick(60) / 1000
        pygame.display.update()
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
