from pygame.sprite import Group
from .entity import Entity
from typing import Tuple, Set, Any
import pygame

class Manager:
    def __init__(
        self,
        screen_size: Tuple[int, int],
        window_caption: str = "My game",
    ):
        self.deltaTime: float = 0.0
        self.WINDOW_SIZE: Tuple[int, int] = screen_size
        self.WIDTH: int = screen_size[0]
        self.HEIGHT: int = screen_size[1]
        self.WORLD_SIZE: Tuple[int, int] = tuple()
        self.ENTITY_LIST: Set[pygame.sprite.Group | Entity] = set()
        self.INPUT_CHART = {}
        self._timers = {}

        pygame.init()
        pygame.display.set_caption(window_caption)
        self.display = pygame.display.set_mode(self.WINDOW_SIZE, pygame.SRCALPHA)

    def Timer(
        self,
        timer_id: str,
        time_interval: int = 1,
    ) -> bool:

        if timer_id not in self._timers:
            self._timers[timer_id] = 0.0
        self._timers[timer_id] += self.deltaTime

        if self._timers[timer_id] >= time_interval:
            self._timers[timer_id] = 0.0
            return True

        return False

class Camera(Entity):
    def __init__(
        self, 
        *groups: Group,
        size: Tuple[int, int],
    ) -> None:
        super().__init__(*groups)
        self.name = 'Camera'
        self.tag = 'camera'
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.direction: pygame.Vector2 = pygame.Vector2()
        self.target_direction: pygame.Vector2 = pygame.Vector2()
        self.refresh()

    def render(
        self,
        entity_list_without_camera,
    ) -> pygame.Surface:
        self.image.fill('black')
        render_entity_list = [e for e in entity_list_without_camera if isinstance(e, Entity)]
        for x in [e.sprites() for e in entity_list_without_camera if isinstance(e, Group)]:
            render_entity_list += x

        for surface in render_entity_list:
            if self.position.x <= surface.rect.right <= self.position.x + self.rect.width and \
            self.position.y <= surface.rect.bottom <= self.position.y + self.rect.height:
                _x = surface.position.x - self.position.x
                _y = surface.position.y - self.position.y
                self.image.blit(surface.image, (_x, _y))
        self.refresh()

        return self.image

    def update(self, deltaTime: float) -> None:
        self.direction = pygame.Vector2(self.axis_smoothing(self.direction.x, self.target_direction.x, deltaTime),
                                        self.axis_smoothing(self.direction.y, self.target_direction.y, deltaTime))
        self.velocity = self.direction * 20
        self.position = self.position + (self.velocity * deltaTime)
        self.refresh()

    def axis_smoothing(self, value, target, dt) -> float:
        # Smooth movement toward target
        if target != 0:
            delta = 8 * dt
        else:
            delta = 8 * dt

        if value < target:
            value = min(value + delta, target)
        elif value > target:
            value = max(value - delta, target)

        return value
