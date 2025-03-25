from random import choice
from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, mask, display
from typing import Tuple, Optional

class Ground(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                speed: float = 10.0,
                frames: list = [],
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position
        self.anchor = anchor
        self.input_chart = {}
        
        self.GROUND = {
            "corner": {
                'up_left': {'frame': frames[0]},
                'down_left': {'frame': frames[4]},
                'up_right': {'frame': frames[10]},
                'down_right': {'frame': frames[14]},
            },
            "anchor": {
                "up": {'frame': frames[5]},
                "down": {'frame': frames[9]},
            }
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

        self.render()
    
    def update(self, deltaTime: float):
        self.kill() if self.position.x + self.image.width//2 < 0 else None
        
        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        direction = 'up'
        tile = self.GROUND['anchor']['up']['frame'].convert_alpha()
        self.image = transform.scale(tile, (40, 40))

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def testing(self, ENVIRONMENT_SHEET) -> list:
        ENVIRONMENT_SHEET_list = []
        for y in range(ENVIRONMENT_SHEET.get_height()//16):
            for x in range(ENVIRONMENT_SHEET.get_width()//16):
                ENVIRONMENT_SHEET_list.append(ENVIRONMENT_SHEET.subsurface((16*x, 16*y, 16, 16)))
        
        for x in ENVIRONMENT_SHEET_list[:]:  # Iterate over a copy to avoid modifying the list while iterating
            if mask.from_surface(x).count() == 0:
                ENVIRONMENT_SHEET_list.remove(x)
        return ENVIRONMENT_SHEET_list