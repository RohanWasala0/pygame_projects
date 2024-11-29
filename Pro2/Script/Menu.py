from pygame import sprite, Vector2, Color, Surface, Rect, Event, draw
from pygame import freetype as ft
from pygame_gui import elements, UI_BUTTON_PRESSED
from pygame_gui.elements.ui_window import UIWindow
from pygame_gui.ui_manager import UIManager

class Menu(sprite.Sprite):
	def __init__(
			self, 
			GameManager,
			position: Vector2 = Vector2(),
			window_size: tuple[int, int] = (0, 0),
			size: tuple[int, int] = (0, 0),
			color: Color = Color('black'),) -> None:
		sprite.Sprite.__init__(self)

		self.GameManager = GameManager
		self.position: Vector2 = position
		self.color: Color = color

		self.init_renderVariables(size, window_size)

		self.inputChart = {
		# UI_BUTTON_PRESSED: {
		# 	self.resetButton: self.GameManager.reset,
		# 	}
		}

	def init_renderVariables(self, size, canvas_size):
		self.image: Surface = Surface(size).convert_alpha()
		self.image.set_colorkey('black')
		self.rect: Rect = self.image.get_rect(center= self.position)
		self.size: tuple[int, int] = self.image.get_size()
		self.color.a = 20
		self.UIManager = UIManager(canvas_size)

		# UI variables
		self.resetButton = elements.UIButton(
			relative_rect= Rect((self.size[0]/2, self.size[1]/2), (100, 50)),
			text= 'Reset',
			manager=self.UIManager)

	def handleInput(self, event: Event):
		"""Handle input events."""
		self.UIManager.process_events(event)

		if not hasattr(event, 'type'):
			return
            
		handlers = self.inputChart.get(event.type)
		if handlers and hasattr(event, 'ui_element'):
			handler = handlers.get(event.ui_element)
			if handler:
				handler()

	def render(self, screenSurface: Surface) -> None:
		# self.GameManager.font.render_to(
		# 	surf= self.image,
		# 	dest= Rect((self.size[0]//2 - 50, self.size[1]//2), (100, 30)),
		# 	text= f'High Score [{self.GameManager.score}]',
		# 	fgcolor= Color('white'),)		

		self.image.fill(self.color)
		self.UIManager.draw_ui(self.image)
		self.rect.center = self.position
		screenSurface.blit(self.image, self.rect)

	def update(self, deltaTime: float) -> None:
		

		self.UIManager.update(deltaTime)


class WindowedMenu(UIWindow):
	def __init__(
		self, 
		GameManager,
		position: Vector2,
		size: tuple[int, int],
		manager: UIManager) -> None:
		super().__init__(
			rect = Rect(position, size), 
			manager = manager, 
			window_display_title = "Menu",
			object_id = "GameMenu",
			visible = 0)

		self.UIManager = manager
		self.size = self.get_container().get_size()
		self.GameManager = GameManager

		self.init_renderVariables()

		self.inputChart = {
		UI_BUTTON_PRESSED: {
			self.resetButton: self.GameManager.reset,
			}
		}

	def init_renderVariables(self) -> None:

		# UI variables
		self.resetButton = elements.UIButton(
			relative_rect= Rect(((self.size[0]/2) - 50, (self.size[1]/2) + 60), (100, 50)),
			text= 'Reset',
			manager=self.UIManager,
			container=self)

	def process_event(self, event: Event) -> bool:
		return super().process_event(event)

		if not hasattr(event, 'type'):
			return
            
		handlers = self.inputChart.get(event.type)
		if handlers and hasattr(event, 'ui_element'):
			handler = handlers.get(event.ui_element)
			if handler:
				handler()

