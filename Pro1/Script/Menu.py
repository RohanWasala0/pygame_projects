import pygame
import pygame_gui
from pygame.sprite import Group
import pygame_gui.ui_manager

from .entities import Entity

class Menu(Entity, pygame.sprite.Sprite):
    def __init__(self, 
            game,
            groups: Group, 
            tag: str, 
            position: pygame.Vector2 = pygame.math.Vector2(), 
            direction: pygame.Vector2 = pygame.math.Vector2(), 
            entitySize: tuple = (0, 0), 
            color: pygame.Color = pygame.Color('black')) -> None:
        super().__init__(groups, tag, position, direction, entitySize, color)
        
        self.game = game
        self.image = pygame.Surface(size=self.entitySize).convert_alpha()
        self.image.set_colorkey('black')
        
        self.UImanager = pygame_gui.UIManager(self.image.get_size())
        self.render()
        
        self.inputChart = {
            pygame_gui.UI_BUTTON_PRESSED: {
                self.resetButton: self.reset,
            }
        }
        
    def render(self):
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=self.position)
        self.resetButton = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(tuple(x/2 for x in self.image.get_size()), (100, 50)),
            text='Reset',
            manager=self.UImanager
        )
        return super().render()

    def reset(self):
        self.game.ball.direction = pygame.math.Vector2()
        self.game.ball.position = pygame.math.Vector2(tuple(x/2 for x in pygame.display.get_window_size()))
        self.game.ball.render()
        self.game.player1_score, self.game.player2_score = 0, 0
        
        
        