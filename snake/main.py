import sys, asyncio
from typing import Iterable, Any

import pygame
from pygame.sprite import Group
from PyG_extras import (
    Manager,
    loop,
    Entity
)
from snake_entity import Snake_Grp
from apple import Apple_Grp

game_manager = Manager(
    screen_size= (1200, 480),
    window_caption= "Py Snake"
)

class Grid(Entity):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface(game_manager.WINDOW_SIZE, pygame.SRCALPHA)
        print(self.image.width)
        for x in range(0, self.image.width, 16):
            pygame.draw.line(self.image, pygame.Color(255, 255, 255, 30), (x, 0), (x, self.image.height))
        for y in range(0, self.image.height, 16):
            pygame.draw.line(self.image, pygame.Color(255, 255, 255, 30), (0, y), (self.image.width, y))
        self.refresh()
game_manager.ENTITY_LIST.add(Grid())

game_manager.ENTITY_LIST.add( snake_group := Snake_Grp(manager= game_manager))
# game_manager.ENTITY_LIST.add(Apple_Grp(manager= game_manager))

game_manager.INPUT_CHART = {
    'discrete': {(pygame.QUIT, pygame.K_ESCAPE): quit},
    'continuous': {
        (pygame.K_UP, pygame.K_w): lambda: setattr(snake_group, 'direction', pygame.Vector2(0, -1)),
        (pygame.K_DOWN, pygame.K_s): lambda: setattr(snake_group, 'direction', pygame.Vector2(0, 1)),
        (pygame.K_LEFT, pygame.K_a): lambda: setattr(snake_group, 'direction', pygame.Vector2(-1, 0)),
        (pygame.K_RIGHT, pygame.K_d): lambda: setattr(snake_group, 'direction', pygame.Vector2(1, 0)),
    },
    'touch': {},
}

def quit():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(loop(
        manager= game_manager,
        fps= 60
    ))