from pygame import (
    Surface,
    SRCALPHA,
    Color,
    sprite,
)
from typing import Tuple, Set, Union
from .entity import Entity

class RenderSystem:
    def __init__(
        self,
        world_size: Tuple[int, int],
        entity_list: Set[Union[sprite.Group, Entity]],
    )->None:
        self.entity_list = entity_list
        self.width, self.height = world_size[0], world_size[1]
        self.world_display: Surface = Surface((self.width, self.height), SRCALPHA)
        self.world_display.fill("black")  # Clear with transparency

    def render(
        self,
        display,
    ) -> None:
        """Clears the world display, draws entities, and blits to main screen."""

        for entity in self.entity_list:
            if not isinstance(entity, sprite.Group) and entity.tag == 'camera':
                e = list(self.entity_list)
                e.remove(entity)
                self.world_display = entity.render(e)

            else:
                if not isinstance(entity, sprite.Group):
                    if hasattr(entity, "image") and hasattr(entity, "rect"):
                        self.world_display.blit(entity.image, entity.rect)
                    else:
                        raise AttributeError("Entity must have 'image' and 'rect' attributes")
                else:
                    entity.draw(self.world_display)

        display.blit(self.world_display, (0, 0))
