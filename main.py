import pygame, sys
import asyncio

from pygame.sprite import Group

from PyG_extras import Manager, loop, Entity, TextCanvas, Camera

game_manager = Manager(
    screen_size= (640, 480)
)
camera = Camera(size= (640, 480))
game_manager.ENTITY_LIST.add(camera)

game_manager.WORLD_SIZE = (1000, 1000)
testing_group = pygame.sprite.Group()
class Square(Entity):
    def __init__(
        self, 
        *groups: pygame.sprite.Group,
        position: pygame.Vector2,
    ) -> None:
        super().__init__(*groups)

        self.image = pygame.Surface((10, 10))
        self.image.fill(pygame.Color('blue'))
        self.position = position
        self.refresh()
for y in range(0, game_manager.WORLD_SIZE[0], 50):
    for x in range(0, game_manager.WORLD_SIZE[1], 50):
        position = pygame.Vector2(x, y)
        Square(testing_group, position = position)

game_manager.ENTITY_LIST.add(testing_group)

game_manager.ENTITY_LIST.add(TextCanvas(
    raw= f"[position: 40, 40][text: testing this engine][color: {pygame.Color('white')}][size: 20][effect: sin_letter]",
    font_path= '04B_03__.TTF',
))

class circle(Entity):
    def __init__(self, *groups: Group) -> None:
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill(pygame.Color('white'))
        pygame.draw.circle(
            self.image,
            pygame.Color('pink'),
            center= (self.image.width//2, self.image.height//2),
            radius= 10,
        )
        self.anchor = 'center'
        self.position = pygame.Vector2(game_manager.WIDTH//2, game_manager.HEIGHT//2)
        self.refresh()

    def update(self, deltaTime: float):
        self.position.x += 10 * deltaTime
        self.refresh()

game_manager.ENTITY_LIST.add(circle())

class testing():
    def __init__(self) -> None:
        self.image: pygame.Surface = pygame.Surface((10, 10))
        self.image.fill(pygame.Color('red'))
        self.rect: pygame.Rect = self.image.get_rect()
# game_manager.ENTITY_LIST.add(testing())

def quit():
    pygame.quit()
    sys.exit()

game_manager.INPUT_CHART = {
    'discrete': {(pygame.QUIT, pygame.K_ESCAPE): quit},
    'continuous': {
        pygame.K_s: lambda: setattr(camera.target_direction, 'y', -1),
        pygame.K_w: lambda: setattr(camera.target_direction, 'y', 1),
        pygame.K_d: lambda: setattr(camera.target_direction, 'x', -1),
        pygame.K_a: lambda: setattr(camera.target_direction, 'x', 1),
        'default': lambda: setattr(camera, 'target_direction', pygame.Vector2()),
    },
    'touch': {},
}

if __name__ == "__main__":
    asyncio.run(loop(
        manager= game_manager,
        fps= 60
    ))