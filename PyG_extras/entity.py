from pygame import Vector2, sprite, Surface, Rect, mask, Color

class Entity(sprite.Sprite):
    def __init__(
        self,
        *groups: sprite.Group,
    ) -> None:
        super().__init__(*groups)  # Add this sprite to the group
        self.name: str = 'entity'
        self.tag: str = 'default'
        self.position: Vector2 = Vector2()
        self.anchor: str = 'topleft'
        self.color: Color = Color(0, 0, 0, 255)
        self.image: Surface = Surface((10, 10))
        self.image.fill(self.color)
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
        self.mask = mask.from_surface(self.image)

    def refresh(
        self
    ) -> None:
        self.image.fill(self.color)
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
        self.mask = mask.from_surface(self.image)


