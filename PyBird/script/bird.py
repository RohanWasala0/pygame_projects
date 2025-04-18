from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, math
from pygame import USEREVENT, time, KEYDOWN, K_SPACE
from typing import Tuple, Optional, List

class Bird(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                position: Optional[Vector2] = None, 
                anchor: str = 'topleft',
                idle: List[Surface] = [],
                flap: List[Surface] = [], 
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.position = position or Vector2()
        self.velocity = Vector2()
        self.gravity = 180
        self.direction = Vector2(0, 1)
        self.anchor = anchor
        
        self.idle = idle
        self.flap = flap
        self.current_animation = 'idle'
        self.animation_event = USEREVENT + abs(hash('animation'))%1000
        self.frame = 0
        time.set_timer(self.animation_event, 200)

        self.input_chart = {
            self.animation_event : self.update_animation,
            KEYDOWN : {K_SPACE: self.flap_action},
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.image.set_colorkey(Color(0, 0, 0, 0))
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
        
    def handling_input(self, event: event) -> None:
        if event_type_action := self.input_chart.get(event.type):
            action = event_type_action if callable(event_type_action) else event_type_action.get(getattr(event, 'key', None)) or \
                     event_type_action.get(getattr(event, 'ui_element', None)) 
            
            if action:
                try:
                    action()
                except Exception as e:
                    print(f"Error executing the action:{action} with error:{e}")
    
    def update(self, deltaTime: float):
        self.direction.y += 0.2
        self.direction.y = math.clamp(self.direction.y, -1, 1)
        self.velocity = self.direction * self.gravity
        position = self.position + (self.velocity * deltaTime)
        self.position = self.position.smoothstep(position, 0.6)
        setattr(self.rect, self.anchor, self.position)
    
    def render(self):
        self.image = transform.scale(self.idle[int(self.frame)], (16*3, 16*3)) if self.current_animation == 'idle' else transform.scale(self.flap[int(self.frame)], (16*3, 16*3))
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
    
    def update_animation(self):
        animation = self.idle if self.current_animation == 'idle' else self.flap
        self.frame += 1
        if self.frame >= len(animation):
            if self.current_animation == 'flap':
                self.current_animation = 'idle'
            self.frame = 0
    
    def flap_action(self):
        setattr(self.direction, 'y', -2)
        if self.current_animation == 'idle':
            self.current_animation = 'flap'
            self.frame = 0
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
