from pygame import sprite, Vector2, event, draw, Color, Surface, Rect

class Entity(sprite.Sprite):
    def __init__(self, 
                tag: str,
                position: Vector2 = Vector2(), 
                entitySize: int = 0, 
                color: list[Color] = [Color('black')],
                pattern: list[list[int]] = []
                ) -> None:
        sprite.Sprite.__init__(self)
        
        self.tag = tag
        self.position = position
        self.entitySize = entitySize
        self.color = color
        self.pattern = pattern
        
        self.collapsed = False
        self.options = []
        
        self.image = Surface((self.entitySize, self.entitySize)).convert_alpha()
        self.image.set_colorkey(Color('black'))
        self.render(pattern)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position.x, self.position.y

    
    def update(self):

        pass
    
    def render(self, pattern: list[list[int]]):
        tile_size = self.entitySize//3
        for row_index, row in enumerate(pattern):
            for column_index, value in enumerate(row):
                color = self.color[value]
                position = (tile_size* column_index, tile_size* row_index)
                draw.rect(self.image, color, Rect(position, (tile_size, tile_size)))
                
    def copy(self, position) -> sprite.Sprite:
        return Entity(
            tag=self.tag,
            position=position,
            entitySize=self.entitySize,
            color=self.color,
            pattern=self.pattern
        )
         