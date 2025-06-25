import re
from pygame import KEYDOWN, K_SPACE, SRCALPHA
from pygame import sprite, Vector2, draw, Color, Surface, Rect, event, font
from typing import Tuple, Optional, Dict, List
import pygame.freetype as ft
import math

class text_canvas(sprite.Sprite):
    def __init__(
        self,
        raw: str,
        groups: sprite.Group = {},
        font_path: str = None,
        anchor: str = 'topleft',
    ) -> None:
        super().__init__(groups)

        self.anchor: str = anchor

        self.font_size: int = 5
        self.align: str = 'left'
        self.text: str = 'Testing'
        self.color: Color = Color('white')
        self.background_color: Color = Color('black')
        self.position: Vector2 = Vector2(0, 0)
        self.padding: float = 0
        self.border_width: float = 0
        self.margin: float = 0
        self.show = 0

        self.time = 0

        self.apply_effect: bool = False
        self.effects_list: list = []
        self._parse(raw)
        self.initial_position = self.position.copy()
        self.ft_font: ft.Font = ft.Font(font_path, self.font_size)
        self.ft_font.pad = False
        self.ft_font.antialiased = True
        self.render()

    def _parse(
        self,
        raw: str,
    ) -> None:
        '''
            [size: int] font_size: int,
            [color: str] color: Color = Color('white'),
            [bg_color: sr] background_color: Color = Color('black'),
            [align: left|center|right] align: str = 'center'
            [text: str] text: str = 'Testing',
            [position: float,float] position: Vector2 = Vector2(), 
            [padding: int] padding: int = 1
            [border: int] border_width: int = 1
            [margin: int] margin: int = 1
            [show_border: 1|0] show: int= 1
            [effect: ] effect: str = None
        '''
        def _position(value: str):
            x, y = map(str, value.strip().split(','))
            x = eval(x, {"__builtins__": None}, {})
            y = eval(y, {"__builtins__": None}, {})
            self.position = Vector2(x, y)
        def _align(value: str):
            if value in ['left', 'center', 'right']:
                self.align = value
            else:
                self.align = 'left'
        # def _text(value: str)
        def _effect(value: str):
            self.apply_effect = True
            self.effects_list = value.strip().split(',')

        pattern = re.compile(r"\[(\w+):\s*([^\]]+)\]")
        matches = pattern.findall(raw)

        dispatch = {
            'align': _align,
            'position': _position,
            'effect': _effect,
            'size': lambda value: setattr(self, 'font_size', int(value)),
            'color': lambda value: setattr(self, 'color', Color(value)),
            'bg_color': lambda value: setattr(self, 'background_color', Color(value)),
            'text': lambda value: setattr(self, 'text', value),
            'padding': lambda value: setattr(self, 'padding', int(value)),
            'border': lambda value: setattr(self, 'border_width', int(value)),
            'margin': lambda value: setattr(self, 'margin', int(value)),
            'show_border': lambda value: setattr(self, 'show', int(value)),
        }

        for key, value in matches:
            handler = dispatch.get(key.lower())
            if handler:
                try:
                    handler(value)
                except:
                    pass

    def update(self, deltaTime: float):
        self.time += 25*deltaTime
        self.effects() if self.apply_effect else None
        self.render()

    def render(self):
        self.list_surfaceText = self.generate_content()
        canvas_size = self.calculate_size(self.list_surfaceText)
        position_list = self.calculate_position(self.list_surfaceText)
        
        self.image = Surface(canvas_size)
        self.image.fill(self.background_color)
        self.image.set_colorkey(Color('black'))
        
        if len(self.list_surfaceText) == len(position_list):
            for line, position in zip(self.list_surfaceText, position_list):
                if self.align == 'center':
                    rect = line.get_rect(center = (self.image.width//2, position[1] + line.height//2))
                elif self.align == 'left':
                    rect = line.get_rect(topleft = position)
                elif self.align == 'right':
                    rect = line.get_rect(topright = (self.image.width - position[0], position[1]))
                self.image.blit(line, rect) 
        
        draw.rect(
            self.image,
            Color('white'),
            self.image.get_rect(),
            width= 1,
            border_radius= 1,
        ) if self.show else None

        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

    def calculate_size(self, surface_list: List[Surface]) -> Tuple[int, int]:
        width = max(line.width for line in surface_list) if surface_list else 0
        width = width + 2*self.margin + 2*self.border_width + 2*self.padding
        # height = sum(line.height for line in surface_list) if surface_list else 0
        
        height = 2*self.margin + self.border_width
        for line in surface_list:
            height += self.border_width + 2*self.padding + line.height
        
        return width, height

    def generate_content(
        self
    ) -> List[Surface]:
        surface_list: List[Surface] = []
        lines = self.text.split('\n')
        for line in lines: 
            text_surf, text_rect = self.ft_font.render(
                text= line,
                fgcolor= self.color,
                bgcolor= self.background_color,
                size= self.font_size,
            )
            draw.rect(
                text_surf,
                Color('white'),
                text_surf.get_rect(),
                width= 1
            ) if self.show else None
            surface_list.append(text_surf)
        return surface_list

    def calculate_position(
        self,
        surface_list: List[Surface]
    ) -> List[Tuple[int, int]]:
        position_list = []
        x = self.border_width + self.padding + self.margin
        y = self.margin + self.border_width + self.padding
        for line in surface_list:
            position_list.append((x, y))
            y += line.height + 2*self.padding + self.border_width
        return position_list

    def effects(self):
        for text_effect in self.effects_list:
            match text_effect.strip():
                case 'letter_sin':
                    self.sinusoidal_motion_per_letter(self.text, 3)
                case 'text_sin':
                    self.sinusoidal_motion(9, 0.18)

    def sinusoidal_motion(self, amplitude: int, frequency: float) -> None:
        sine = amplitude * math.sin(frequency * self.time)
        self.position = Vector2(self.position.x, self.initial_position.y + sine)

    def sinusoidal_motion_per_letter(
        self,
        text: str,
        sin: int,
    ) -> None:
        text = list(text)
        for index, letter in enumerate(text):
            ...