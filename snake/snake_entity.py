from typing import Any, Iterable
from pygame.sprite import AbstractGroup, Group
from pygame import (
    Surface,
    SRCALPHA,
    Color,
    Vector2
)
from PyG_extras import Entity, Manager

class Snake(Entity):
    def __init__(
        self, 
        *groups: Group,
        position: Vector2,
        manager: Manager,
    ) -> None:
        super().__init__(*groups)

        self.tag = 'snake'
        self.image = Surface((16, 16), SRCALPHA)
        self.color = Color('blue')
        self.position = position
        self.refresh()
        self.manager = manager

class Snake_Grp(Group):
    def __init__(
        self, 
        *sprites: Any | AbstractGroup | Iterable, 
        manager: Manager
    ) -> None:
        super().__init__(*sprites)
        self.manager = manager
        self.length: int = 10
        self.direction: Vector2 = Vector2()
        self.add_body()

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.length = len(self.sprites())
        if self.manager.Timer('move'):            
            head: Entity = self.sprites()[-1]
            target_position = head.position
            head.position = head.position + (self.direction * 16)
            head.refresh()
            if self.length > 1 and target_position != head.position:
                for s in self.sprites()[:-1]:
                    temp = s.position
                    s.position = target_position
                    target_position = temp 
                    s.refresh()
            # print([x.position for x in self.sprites()])
                
        return super().update(*args, **kwargs)

    def add_body(
        self
    ) -> None:
        self.empty()
        for x in range(self.length):
            position = self.sprites()[0].position if len(self.sprites()) > 0 else Vector2(32, 32)
            Snake(
                self,
                position= Vector2(position.x+(x*16), position.y),
                manager= self.manager
            )
