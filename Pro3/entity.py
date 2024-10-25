from pygame import sprite, Vector2, event, draw, Color, Surface, math, display, transform
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, mouse, KEYDOWN, K_SPACE
from math import atan2, degrees

class Entity(sprite.Sprite):
    def __init__(self, 
                tag: str,
                groups: sprite.Group,
                position: Vector2 = Vector2(), 
                direction: Vector2 = Vector2(1, 0), 
                entitySize: tuple = (20, 10), 
                color: Color = Color('black')) -> None:
        super().__init__(groups)
        
        self.tag = tag
        self.group = groups
        self.entitySize = entitySize
        self.color = color
        
        self._window_size = display.get_window_size()
        # Tune these parameters for different flocking behaviors
        self.max_speed = 200
        self.min_speed = 100
        self.max_force = 1.9  # Maximum steering force
        
        # Initialize position and movement variables
        self.position = Vector2(position)
        self.direction = direction.normalize()
        self.velocity = self.direction * self.get_random_speed()
        
        self.weights = [1.5, 1.0, 1.0]
        # Weights for different behaviors
        self.separation_weight = self.weights[0]
        self.alignment_weight = self.weights[1]
        self.cohesion_weight = self.weights[2]
        self.seek_weight = 2
        
        # Vision parameters
        self.vision_radius = 80
        self.separation_radius = 50  # Smaller radius for separation
        self.arrival_radius = 100
        
        #Target seeking
        self.is_seeking = False
        self.target_position = None
        
        #Custom inputchart for pygame
        self.inputChart = {
            MOUSEBUTTONDOWN: lambda: self.set_target(mouse.get_pos()),
            MOUSEBUTTONUP: lambda: self.set_target(None, False),

        }
        # Setup sprite image
        self.image = Surface(self.entitySize).convert_alpha()
        self.image.set_colorkey('black')
        self.ogImage = self.image.copy()
        self.render()
        
    def get_random_speed(self):
        from random import uniform
        return uniform(self.min_speed, self.max_speed)
    
    def update(self, deltaTime: float, targetPos: Vector2 = None):
        # Calculate flocking forces
        separation = self.separation() * self.separation_weight
        alignment = self.alignment() * self.alignment_weight
        cohesion = self.cohesion() * self.cohesion_weight
        seek = self.seek() * self.seek_weight
        
        # Apply all forces
        acceleration = separation + alignment + cohesion + seek
        
        # Update velocity
        self.velocity += acceleration
        
        # Limit speed
        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)
        elif speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)
            
        # Update position and direction
        self.position += self.velocity * deltaTime
        if self.velocity.length() > 0:
            self.direction = self.velocity.normalize()
        
        self.checkBoundaries()
        
        # Update sprite rotation
        angle = degrees(atan2(-self.direction.y, self.direction.x))
        self.image = transform.rotate(self.ogImage, angle)
        self.rect = self.image.get_rect(center=self.position)
    
    def handleInput(self, event: event) -> None:
        #Handle input events 
        if hasattr(event, 'type') and event.type in self.inputChart:
            if hasattr(event, 'key') and event.key in self.inputChart[event.type]:    
                self.inputChart[event.type][event.key]()
            elif hasattr(event, 'ui_element') and event.ui_element in self.inputChart[event.type]:
                self.inputChart[event.type][event.ui_element]()
            else:
                self.inputChart[event.type]() 
            
    def render(self):
        # Draw triangle shape for boid
        draw.polygon(self.ogImage, self.color, [
            (0, 0),
            (self.entitySize[0], self.entitySize[1]/2),
            (0, self.entitySize[1]),
            (5, self.entitySize[1]/2)
        ])
        self.rect = self.ogImage.get_rect(center=self.position)
    
    def checkBoundaries(self):
        # Wrap around screen edges
        if self.position.x < 0:
            self.position.x = self._window_size[0]
        elif self.position.x > self._window_size[0]:
            self.position.x = 0

        if self.position.y < 0:
            self.position.y = self._window_size[1]
        elif self.position.y > self._window_size[1]:
            self.position.y = 0
    
    def steer_towards(self, target: Vector2) -> Vector2:
        """Helper function to calculate steering force towards a target"""
        if isinstance(target, tuple):
            target = Vector2(target)
            
        desired = target - self.position
        if desired.length() > 0:
            desired = desired.normalize() * self.max_speed
            steer = desired - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer
        return Vector2(0, 0)
            
    def separation(self) -> Vector2:
        """Keep distance from other boids"""
        steering = Vector2()
        total = 0
        
        for other in self.group.sprites():
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < self.separation_radius:
                    diff = self.position - other.position
                    if diff.length() > 0:
                        diff = diff.normalize() / max(distance, 1)  # Weight by distance
                        steering += diff
                        total += 1
        
        if total > 0:
            steering /= total
            if steering.length() > 0:
                steering = steering.normalize() * self.max_speed
                steering -= self.velocity
                if steering.length() > self.max_force:
                    steering.scale_to_length(self.max_force)
                
        return steering

    def alignment(self) -> Vector2:
        """Match velocity with nearby boids"""
        steering = Vector2()
        total = 0
        
        for other in self.group.sprites():
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < self.vision_radius:
                    steering += other.velocity
                    total += 1
        
        if total > 0:
            steering /= total
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            if steering.length() > self.max_force:
                steering.scale_to_length(self.max_force)
            
        return steering

    def cohesion(self) -> Vector2:
        """Move towards average position of nearby boids"""
        center = Vector2()
        total = 0
        
        for other in self.group.sprites():
            if other != self:
                distance = self.position.distance_to(other.position)
                if distance < self.vision_radius:
                    center += other.position
                    total += 1
        
        if total > 0:
            center /= total
            return self.steer_towards(center)
            
        return Vector2(0, 0)
    
    def set_target(self, target_position: Vector2 | tuple, enable_seeking: bool = True):
        """Set a target position for the entity to seek"""
        if isinstance(target_position, tuple):
            target_position = Vector2(target_position)
        self.target_position = target_position
        self.is_seeking = enable_seeking
        
    def seek(self) -> Vector2:
        """Generate steering force to seek target position"""
        if not self.is_seeking or self.target_position is None:
            return Vector2(0, 0)
        
        # Calculate distance to target
        distance = self.position.distance_to(self.target_position)
        
        # Get basic steering direction
        desired = self.target_position - self.position
        if desired.length() > 0:
            desired = desired.normalize()
            
            # Implement arrival behavior
            if distance < self.arrival_radius:
                # Scale speed based on distance to target
                speed = self.max_speed * (distance / self.arrival_radius)
                speed = max(speed, self.min_speed)
            else:
                speed = self.max_speed
                
            desired *= speed
            
            # Calculate steering force
            steer = desired - self.velocity
            if steer.length() > self.max_force:
                steer.scale_to_length(self.max_force)
            return steer
            
        return Vector2(0, 0)