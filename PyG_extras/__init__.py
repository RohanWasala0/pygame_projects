import pygame
import asyncio

from .input_manager import InputManager
from .text_canvas import TextCanvas
from .manager import Manager, Camera
from .entity import Entity
from .render import RenderSystem
from .update import UpdateSystem

__version__ = '1.0.0'
__all__ = ["InputManager", "TextCanvas", "Manager", "Entity", "RenderSystem", "UpdateSystem", "Camera"]

async def loop(
    manager: Manager,
    fps: float,
) -> None:
    clock = pygame.time.Clock()
    while True:

        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        InputManager(events, keys, manager.INPUT_CHART)

        RenderSystem(
            world_size= manager.WINDOW_SIZE,
            entity_list= manager.ENTITY_LIST
        ).render(manager.display)
        updateSystem = UpdateSystem()

        for entity in manager.ENTITY_LIST:
            updateSystem.update(entity, manager.deltaTime)

        manager.deltaTime = clock.tick(fps) / 1000
        pygame.display.update()
        await asyncio.sleep(0)