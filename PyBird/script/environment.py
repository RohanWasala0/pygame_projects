from random import choice
from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, mask, display
from typing import Tuple, Optional

class Environment(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                BACKGROUND_AIR: list = [],
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.anchor = anchor
        self.input_chart = {}
        
        self.AIR = {
            '_01': {'frames': BACKGROUND_AIR[0]},
            '_02': {'frames': self.merge_surfaces(BACKGROUND_AIR[1], BACKGROUND_AIR[2])},
            '_03': {'frames': self.merge_surfaces(BACKGROUND_AIR[3], BACKGROUND_AIR[4])},
            '_04': {'frames': self.merge_surfaces(BACKGROUND_AIR[5], BACKGROUND_AIR[6])},
            '_05': {'frames': self.merge_surfaces(BACKGROUND_AIR[7], BACKGROUND_AIR[8])},
            '_06': {'frames': self.merge_surfaces(BACKGROUND_AIR[9], BACKGROUND_AIR[10])},
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

        self.render()
    
    def update(self, deltaTime: float):
        self.frame += 0.05
        if self.frame >= len(self.animation_list):
            self.frame = 0
        # setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        air_type = self.AIR[choice(list(self.AIR.keys()))]['frames']
        size = tuple(x*4 for x in air_type.size) 
        temp = transform.scale(air_type.convert_alpha(), size)
        self.image = transform.flip(temp, True, False)
        # print(int(self.frame))
        # self.image.fill(Color(0, 0, 0, 0))

        draw.rect(
            self.image, 
            Color('white'),
            self.image.get_rect(),
            width=1,
        )

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    # def dividing_sheet(self) -> None:
    #     idle_sheet = Surface((16*2, 16))
    #     jump_sheet = Surface((16*4, 16))

    #     idle_sheet.blit(self.sheet, (0, 0), (0, 0, 16*2, 16))
    #     jump_sheet.blit(self.sheet, (0, 0), (16*3, 0, 16*4, 16))

    #     self.idle_animation_list = []
    #     self.jump_animation_list = []

    #     for x in range(2):
    #         self.idle_animation_list.append(transform.scale(idle_sheet.subsurface((16*x, 0, 16, 16)), (16*4, 16*4)))
    #     for y in range(4):
    #         self.jump_animation_list.append(transform.scale(jump_sheet.subsurface((16*y, 0, 16, 16)), (16*4, 16*4)))

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