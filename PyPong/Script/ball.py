from pygame import (
    sprite,
    Vector2,
    mask,
    draw,
    Color,
    Surface,
    display,
    KEYDOWN,
    K_SPACE,
    SRCALPHA,
    Rect,
    FINGERUP,
)

from input_manager import InputManager

from math import radians, sin, cos
from random import uniform
from typing import Tuple, Optional

class Ball(sprite.Sprite):
    def __init__(
        self,
        groups: sprite.Group,
        anchor: str = 'topleft',
        position: Optional[Vector2] = Vector2(),
        radius: int = 1,
        color: Color = Color('white'),
    ) -> None:
        super().__init__(groups)
        
        self.color = color
        self.group = groups
        self.radius = radius
        self.anchor = anchor
        self.dimensions = (2*radius, 2*radius)
        self.position = position or Vector2()
        self.input_manager = InputManager()

        self.trail = []
        self.max_trail = 20

        self.velocity = Vector2()
        self.speed = 400
        self.start = True

        self.input_manager.input_chart = {
            'discrete': {
                KEYDOWN: {
                    K_SPACE: lambda: setattr(self, 'velocity', self.rand_velocity())
                }
            },
            'touch': {
                    FINGERUP: lambda event: setattr(self, 'velocity', self.rand_velocity())
                }

        }
        
        self.render()

    def update(self, deltaTime: float) -> None:
        # self.conditions()
        self.collision_walls()

        self.position = self.position + (self.velocity * deltaTime)

        self.trail.append((int(self.position.x), int(self.position.y)))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
        self.render()

    def render(self) -> None:
        """
        Creates the visual representation of entity
        Makes pygame.Surface converts it alpha so that entity's alpha can be used
        Set colorkey to black and fills it with the same color to make it transparent
        """
        self.image = Surface(self.dimensions).convert_alpha()
        self.image.set_colorkey(Color('black'))
        self.image.fill(Color('black'))

        draw.circle(
            surface= self.image,
            color= self.color,
            center= (self.radius, self.radius),
            radius= self.radius,
        )

        self.rect = self.image.get_rect()
        self.mask = mask.from_surface(self.image)
        setattr(self.rect, self.anchor, self.position)

    def collision_walls(self) -> None:
        WIDTH, HEIGHT = display.get_window_size()
        # # Left wall
        # if self.position.x - self.radius <= 0:
        #     self.position.x = self.radius
        #     self.velocity.x = -self.velocity.x 

        # # Right wall
        # if self.position.x + self.radius >= WIDTH:
        #     self.position.x = WIDTH - self.radius
        #     self.velocity.x = -self.velocity.x 

        # Top wall
        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y = -self.velocity.y 

        # Bottom wall
        if self.position.y + self.radius >= HEIGHT:
            self.position.y = HEIGHT - self.radius
            self.velocity.y = -self.velocity.y

    def rand_velocity(self) -> Vector2:
        while True:
            direction = Vector2(uniform(-1, 1), uniform(-1, 1))
            return direction.normalize() * self.speed

    def change_angle(self, angles: Tuple[int, int]) -> Vector2:
        angle = uniform(radians(angles[0]), radians(angles[1]))
        return Vector2(cos(angle), sin(angle)).normalize() * self.speed

    def reset(self) -> None:
        WIDTH, HEIGHT = display.get_window_size()
        self.velocity = Vector2()
        self.position = Vector2(WIDTH//2, HEIGHT//2)
        setattr(self.rect, self.anchor, self.position)
        self.input_manager.input_chart['touch'] = {
            FINGERUP: lambda event: setattr(self, 'velocity', self.rand_velocity())
        }

        # self.rect = self.rect.move_to(center= Vector2(tuple(x/2 for x in display.get_window_size())))

    def test(self):
        print("testing, successful")

    def reflect_on_collision(self, object):
        future_position = self.position + self.velocity.normalize() if self.velocity.length() != 0 else self.position
        object_rect: Rect = object.rect

        # Get closest point on square to ball center
        closest_x =  max(object_rect.left, min(future_position.x, object_rect.right))
        closest_y = max(object_rect.top, min(future_position.y, object_rect.bottom))

        # Calculate distance from ball center to closest point
        distance_vec = future_position - Vector2(closest_x, closest_y)
        distance = distance_vec.length()

        # Check collision
        if sprite.collide_mask(object, self) and distance < self.radius:
            # Calculate collision normal
            if distance == 0:
                # Ball is exactly at the closest point, use a default normal
                normal = Vector2(0, 1)
            else:
                normal = distance_vec.normalize()

            # Move ball out of collision
            overlap = self.radius - distance
            self.position += normal * overlap

            if normal.x in [-1, 0, 1] and normal.y in [-1, 0, 1]:
                self.velocity = self.velocity.reflect(normal) 
            return True
        return False

    def draw_trail(self, screen):
        for i, position in enumerate(self.trail):
            alpha = i/len(self.trail)
            trail_color = (int(self.color[0] * alpha), 
                          int(self.color[1] * alpha), 
                          int(self.color[2] * alpha))
            draw.circle(screen, trail_color, position, max(1, int(self.radius * alpha * 0.75)))

    def velocity_vector(self, screen):
        # Draw velocity vector (for visualization)
        if self.velocity.length() > 0:
            end_x = int(self.position.x + self.velocity.normalize().x * self.speed//50)
            end_y = int(self.position.y + self.velocity.normalize().y * self.speed//50)
        else:
            end_x, end_y = 0, 0
        draw.line(screen, Color('white'), (int(self.position.x), int(self.position.y)), (end_x, end_y), 2)