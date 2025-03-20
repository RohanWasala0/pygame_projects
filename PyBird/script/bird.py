from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform
from typing import Tuple, Optional

class Bird(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                sheet: Surface = Surface((0, 0)), 
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.anchor = anchor
        self.sheet = sheet
        self.frame = 0
        self.dividing_sheet()
        
        self.input_chart = {}
        
        self.image: Surface = Surface((16, 16), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
        
    def handling_input(self, event: event) -> None:
        """
        Handles input events the corresponding action from the input chart.
        Attempt to find for the specific key, ui_element, etc
        If the action exist in the input chart execute the mapped action 
        """
        if event_type_action := self.input_chart.get(event.type):
            action = event_type_action.get(getattr(event, 'key', None)) or \
                     event_type_action.get(getattr(event, 'ui_element', None))
            
            if action:
                try:
                    action()
                except Exception as e:
                    print(f"Error executing the action:{action} with error:{e}")
    
    def update(self, deltaTime: float):
        self.frame += 0.05
        if self.frame >= len(self.idle_animation_list):
            self.frame = 0
        # setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        self.image = self.idle_animation_list[int(self.frame)]
        self.image.set_colorkey(Color(0, 0, 0, 0))
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
    
    def dividing_sheet(self) -> None:
        idle_sheet = Surface((16*2, 16))
        jump_sheet = Surface((16*4, 16))

        idle_sheet.blit(self.sheet, (0, 0), (0, 0, 16*2, 16))
        jump_sheet.blit(self.sheet, (0, 0), (16*3, 0, 16*4, 16))

        self.idle_animation_list = []
        self.jump_animation_list = []

        for x in range(2):
            self.idle_animation_list.append(transform.scale(idle_sheet.subsurface((16*x, 0, 16, 16)), (16*4, 16*4)))
        for y in range(4):
            self.jump_animation_list.append(transform.scale(jump_sheet.subsurface((16*y, 0, 16, 16)), (16*4, 16*4)))
