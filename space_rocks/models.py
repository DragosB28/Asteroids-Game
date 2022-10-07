from pygame.math import Vector2
from pygame.transform import rotozoom

from utils import load_sprite, wrap_position, get_random_velocity, load_sound

UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.velocity = Vector2(velocity)
        self.radius = sprite.get_width() / 2

    def draw(self, surface):
        blit_position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        if distance < self.radius + other_obj.radius:
            return True
        else:
            return False

class Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 3

    def __init__(self, position, create_bullet_callback, rocket_type="default_rocket"):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("laser")
        self.rocket_type = load_sprite(rocket_type)
        self.direction = Vector2(UP)
        super().__init__(position, self.rocket_type, Vector2(0))

    def rotate(self, clockwise=True):
        if clockwise:
            sign = 1
        else:
            sign = -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3, asteroid="asteroid_default"):
        self.create_asteroid_callback = create_asteroid_callback
        self.size = size
        self.asteroid_type = load_sprite(asteroid)

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(self.asteroid_type, 0, scale)

        super().__init__(
            position, sprite, get_random_velocity(1, 3)
        )

    def split(self, asteroid_t):
        if self.size > 1:
            for _ in range(2):
                asteroid = Asteroid(
                    self.position, self.create_asteroid_callback, self.size - 1, asteroid_t
                )
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

    def move(self, surface):
        self.position = self.position + self.velocity