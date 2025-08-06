from pygame import sprite
from typing import Set

class UpdateSystem():
    def update(
        self,
        entity,
        deltaTime: float
    ) -> None:

        if not isinstance(entity, sprite.Group):
            if hasattr(entity, "update"):
                entity.update(deltaTime)
            else:
                raise AttributeError("Entity must have 'image' and 'rect' attributes")
        else:
            if isinstance(entity, sprite.Group):
                entity.update(deltaTime)
                # for s in entity.sprites():
                #     s.update(deltaTime)