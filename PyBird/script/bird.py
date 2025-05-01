from pygame import sprite, Vector2, event, Rect, Color, Surface, SRCALPHA, draw, transform, math
from pygame import USEREVENT, mask, KEYDOWN, K_SPACE
from typing import Tuple, Optional, List, Dict

class Bird(sprite.Sprite):
    def __init__(self, 
                groups: sprite.Group,
                idle_animation_list: List[Surface],
                flap_animation_list: List[Surface], 
                position: Vector2 = Vector2(), 
                anchor: str = 'topleft',
                scale: float = 1,
                ) -> None:
        super().__init__(groups)
        
        self.group = groups
        self.anchor: str = anchor
        self.scale: float = scale
        self.gravity: float = 100
        self.jump_factor: int = -300
        self.position: Vector2 = position or Vector2()
        self.velocity: Vector2 = Vector2()
        self.scaled_size = tuple([dimension* scale for dimension in idle_animation_list[0].size])
        
        self.frame: int = 0
        self.current_animation: str = 'flap'
        self.animation_chart: Dict[str, AnimatedObject] = {
            'idle': AnimatedObject(idle_animation_list, 100),
            'flap': AnimatedObject(flap_animation_list, 50),
        }        

        self.input_chart = {
            KEYDOWN : {K_SPACE: self.flap_action},
        }
        
        self.image: Surface = Surface((0, 0), SRCALPHA)
        self.render()
        self.animated_object: AnimatedObject = self.animation_chart[self.current_animation]
        self.mask = mask.from_surface(self.image)
        
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
        self.gravity += 10 
        self.gravity = math.clamp(self.gravity, 100, 800)
        self.velocity.y += self.gravity * deltaTime
        self.position += self.velocity * deltaTime
        
        self.animated_object.play(deltaTime)
        self.image = transform.scale(self.animated_object.current_frame, self.scaled_size)
        self.rect: Rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
        self.mask = mask.from_surface(self.image)
        # self.image.blit(self.mask.to_surface())
    
    def render(self):
        self.image = transform.scale(self.animation_chart[self.current_animation].current_frame, self.scaled_size)
        self.image.set_colorkey(Color(0, 0, 0, 0))

        draw.rect(
            self.image, 
            Color('white'),
            self.image.get_rect(),
            width=1,
        )

        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)
    
    def flap_action(self):
        self.velocity.y = self.jump_factor
        
        # self.change_animation(
        #     _from = 'idle',
        #     _to = 'flap'
        # )
        # self.animation_chart[self.current_animation].play()
    
    def change_animation(
            self,
            _from: str,
            _to: str,
    ):
        if self.current_animation != _from or self.current_animation == _to:
            return 
        
        current_animation: AnimatedObject = self.animation_chart[_from]
        if current_animation.animation_completed:
            current_animation.reset()
            self.current_animation = _to
            self.animation_chart[_to].reset()
            # self.animation_chart[_to].reset()
            print("changed")
            return
        else:
            current_animation.loop = False
            # self.change_animation(_from, _to)
        


class AnimatedObject:
    def __init__(
            self,
            frames: List[Surface],
            duration: int,
            loop: bool = True,
    ):
        self.index: int = 0
        self.loop: bool = loop
        self.running: bool = True
        self.duration: int = duration
        self.animation_timer: float = 0.0 
        self.frames: List[Surface] = frames
        self.animation_completed: bool = False
        self.current_frame: Surface = self.frames[self.index]

    def play(
            self,
            deltaTime: float,
    ) -> None:
        if not self.running or self.animation_completed: 
            return
        
        self.animation_timer += 1
        if self.animation_timer >= self.duration:
            self.animation_timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.animation_completed = True
                    self.running = False
            self.current_frame = self.frames[self.index]
    
    def stop(
            self,
    ) -> None:
        self.running = False

    def reset(
            self,
    ) -> None:
        self.frame = 0
        self.current_frame = self.frames[self.frame]
        self.animation_timer = 0
        self.running = True
        self.animation_completed = False
        