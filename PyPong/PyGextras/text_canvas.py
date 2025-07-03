import re
from pygame import KEYDOWN, K_SPACE, SRCALPHA, BLEND_RGB_MULT, BLEND_RGBA_MULT
from pygame import sprite, Vector2, draw, Color, Surface, Rect, event, font, mask, font
from typing import Tuple, Optional, Dict, List
import pygame.freetype as ft
import math
global alphabet

alphabet = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W",
    "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
    "u", "v", "w", "x", "y", "z", ".", "-", ",", ":", "'", "!", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    " ", "(", ")", "+", "/", "%",
]
class TextCanvas(sprite.Sprite):
    def __init__(
        self,
        raw: str,
        groups: sprite.Group = {},
        font_path: str = None,
        font_size: int = 5,
        tag: str = '',
        anchor: str = 'topleft',
    ) -> None:
        super().__init__(groups)

        self.anchor: str = anchor
        self.tag: str = tag
        self.raw: str = raw

        self.font_path = font_path
        self.font_size = font_size
        self.align: str = 'left'
        self.text: str = 'Testing'
        self.color: Color = Color('white')
        self.background_color: Color = Color('black')
        self.position: Vector2 = Vector2(0, 0)
        self.padding: float = 0
        self.border_width: float = 0
        self.margin: float = 0
        self.debug = 0

        self.time = 0

        self.effects_list: list = [] 
        self._init_font()

        self._parse(self.raw)
        
        self.rendered_text: Surface = Surface((0, 0))
        self.render()

    def _init_font(self):
        self.letters: Dict[str, Surface]= {} 
        self.ft_font = font.Font(self.font_path, self.font_size)

        global alphabet
        for char in alphabet:
            char_img = self.ft_font.render(char, antialias= True, color= (255, 255, 255), bgcolor=(0, 0, 0))
            char_img.set_colorkey(Color(0, 0, 0))
            draw.rect(char_img, Color('white'), char_img.get_rect(), 1) if self.debug else None
            self.letters[char] = char_img

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
            for e in value.strip().split(','):
                self.effects_list.append(e.strip())

        pattern = re.compile(r"\[(\w+):\s*([^\]]+)\]")
        matches = pattern.findall(raw)

        dispatch = {
            'align': _align,
            'position': _position,
            'effect': _effect,
            'color': lambda value: setattr(self, 'color', Color(value)),
            'bg_color': lambda value: setattr(self, 'background_color', Color(value)),
            'text': lambda value: setattr(self, 'text', value),
            'padding': lambda value: setattr(self, 'padding', int(value)),
            'border': lambda value: setattr(self, 'border_width', int(value)),
            'margin': lambda value: setattr(self, 'margin', int(value)),
            'debug': lambda value: setattr(self, 'debug', int(value)),
        }

        for key, value in matches:
            handler = dispatch.get(key.lower())
            if handler:
                try: handler(value)
                except: pass

    def update(self, deltaTime: float):
        self.time += 50 * deltaTime
        self.effects(self.effects_list)
        self.render()

    def render(self): 
        # self._parse(self.raw)
        
        # self.rendered_text: Surface = Surface((0, 0))
        self.image = self.effects(self.effects_list)
        # self.image.fill(self.background_color)
        # self.image.set_colorkey(Color('black'))
        self.image.blit(self.rendered_text)
        
        draw.rect(
            self.image,
            Color('white'),
            self.image.get_rect(),
            width= 1,
            border_radius= 1,
        ) if self.debug else None

        self.rect = self.image.get_rect()
        setattr(self.rect, self.anchor, self.position)

    def calculate_size(self, offset: Vector2) -> Tuple[int, int]:
        surface_list = self.text.split('\n')
        width = max(sum(self.letters[letter].width for letter in line) for line in surface_list)
        width += 2 * self.margin + 2 * self.border_width + 2 * self.padding 

        y_offset = (self.border_width + 2*self.padding)
        height = 2*self.margin + self.border_width
        height += sum(max(self.letters[letter].height for letter in line) + y_offset for line in surface_list) + 2*offset.y

        return width, height

    def effects(self, effects_list: List[str]) -> Surface:
        def shadow(surface: Surface, color: Color, offset: Vector2 = Vector2(0, 1)):
            result_surface = Surface((surface.width + 2, surface.height + 2))
            result_surface.set_colorkey((0, 0, 0))

            _mask = mask.from_surface(surface)
            mask_surf = _mask.to_surface()
            mask_surf.set_colorkey((0, 0, 0))
            mask_surf.fill(color, special_flags=BLEND_RGB_MULT)

            result_surface.blit(mask_surf, (1 + offset.x, 1 + offset.y))
            result_surface.blit(surface, (1, 1))
            return result_surface
        def sin_per_letter(index: int, position: Vector2, amplitude: int, frequency: float) -> Vector2:
            offset: Vector2 = Vector2()
            phase_offset = index*frequency
            offset.y += math.sin((phase_offset + self.time)/10) * amplitude
            return Vector2(position.x, position.y + offset.y)

        _size = self.calculate_size(Vector2(5, 5))
        rendered_text = Surface(_size, SRCALPHA)
        start_position = Vector2(self.border_width + self.padding + self.margin, self.margin + self.border_width + self.padding + 5)

        for line in self.text.split('\n'):
            for index, letter in enumerate(line):
                result_surface, result_position = self.letters[letter], start_position
                result_surface = shadow(result_surface, Color(10, 10, 10), Vector2(5, 5)) if 'shadow' in effects_list else self.letters[letter]
                result_position = sin_per_letter(index, result_position, 5, 5) if 'sin_letter' in effects_list else result_position
                # result_rect = self.letters[letter].get_rect(topleft = Vector2(start_position.x, start_position.y))

                rendered_text.blit(result_surface, result_position)
                start_position.x += self.letters[letter].width

            start_position.x = self.border_width + self.padding + self.margin
            start_position.y += result_surface.height + 2*self.padding + self.border_width # move to next line

        return rendered_text