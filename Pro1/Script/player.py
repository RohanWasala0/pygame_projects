import pygame

from entities import Entity

class Player(Entity):
    def __init__(self, tag: str, position: list, input_keys: list) -> None:
        super().__init__(tag, position)
        self.InputChart = {
            pygame.KEYDOWN: {
                input_keys[0] : lambda: setattr(self, "Y_movement_bool", (True, self.Y_movement_bool[1])),
                input_keys[1] : lambda: setattr(self, "Y_movement_bool", (self.Y_movement_bool[0], True)),
                },
            pygame.KEYUP: {
                input_keys[0] : lambda: setattr(self, "Y_movement_bool", (False, self.Y_movement_bool[1])),
                input_keys[1] : lambda: setattr(self, "Y_movement_bool", (self.Y_movement_bool[0], False)),
                },
        }
