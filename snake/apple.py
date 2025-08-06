from pygame import (
    sprite,
    Vector2,
    Surface,
    SRCALPHA
)
from PyG_extras import Entity, Manager
from typing import Any, Iterable
from random import randrange

class Apple(Entity):
    def __init__(
        self,
        *groups: sprite.Group,
        position: Vector2
    ) -> None:
        super().__init__(*groups)
        self.tag = 'apple'
        self.image = Surface((16, 16), SRCALPHA)
        self.image.fill('red')
        self.position = position
        self.refresh()

class Apple_Grp(sprite.Group):
    def __init__(
        self, 
        *sprites: Any | sprite.AbstractGroup | Iterable,
        manager: Manager
    ) -> None:
        super().__init__(*sprites)
        self.manager = manager

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.manager.Timer('spawn apple', 4):
            position = Vector2(randrange(0, self.manager.WIDTH, 16), randrange(0, self.manager.HEIGHT, 16))
            Apple(
                self,
                position= position
            )
        return super().update(*args, **kwargs)