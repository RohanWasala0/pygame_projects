from random import choice, randrange
from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, mask, display
from typing import Tuple, Optional

class Environment(sprite.Sprite):
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
        self.size = 2
        self.count = 10
        self.velocity = Vector2(-1, 0) * speed
        
        self.AIR = {
            '_01': {'frames': frames[0]},
            '_02': {'frames': self.merge_surfaces(frames[1], frames[2])},
            '_03': {'frames': self.merge_surfaces(frames[3], frames[4])},
            '_04': {'frames': self.merge_surfaces(frames[5], frames[6])},
            '_05': {'frames': self.merge_surfaces(frames[7], frames[8])},
            '_06': {'frames': self.merge_surfaces(frames[9], frames[10])},
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

        self.render()
    
    def update(self, deltaTime: float):
        # self.frame += 0.05
        # if self.frame >= len(self.animation_list):
        #     self.frame = 0
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
        air_type = self.AIR[choice(list(self.AIR.keys()))]['frames'].convert_alpha()
        size = tuple(x*self.size for x in air_type.size) 
        scaled = transform.scale(air_type, size)
        self.image = transform.flip(scaled, True, False)
        self.image.set_alpha(55)

        # draw.rect(
        #     self.image, 
        #     Color('white'),
        #     self.image.get_rect(),
        #     width=1,
        # )

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def merge_surfaces(self, surface1, surface2):
        new_surface = Surface((16*2, 16), SRCALPHA)
        new_surface.blit(surface1, (0, 0))
        new_surface.blit(surface2, (16, 0))
        return new_surface

    def testing(self, ENVIRONMENT_SHEET) -> list:
        ENVIRONMENT_SHEET_list = []
        for y in range(ENVIRONMENT_SHEET.get_height()//16):
            for x in range(ENVIRONMENT_SHEET.get_width()//16):
                ENVIRONMENT_SHEET_list.append(ENVIRONMENT_SHEET.subsurface((16*x, 16*y, 16, 16)))
        
        for x in ENVIRONMENT_SHEET_list[:]:  # Iterate over a copy to avoid modifying the list while iterating
            if mask.from_surface(x).count() == 0:
                ENVIRONMENT_SHEET_list.remove(x)
        return ENVIRONMENT_SHEET_list