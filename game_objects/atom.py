from imports import *
from game_objects.atom_container import *
from engine import *

class Atom(object):
    def __init__(self,
                 radius: int = 50,
                 color: pg.Color = pg.Color(255, 255, 255, 255),
                 pos: Tuple[float, float] = (0.0, 0.0),
                 velocity: Tuple[float, float] = (2.0, 2.0),
                 local_angle: int = 0,
                 tolerance: float = -1,
                 mass: int = 1):

        # Colors
        self.color: pg.Color = color
        self.current_color: pg.Color = self.color

        # Scalars
        self.radius: float = radius
        self.mass: int = mass
        self.local_angle: float = local_angle
        self.tolerance: float = self.radius / 10 if tolerance == -1 else tolerance * self.radius
        print(self.tolerance)
        self.__max_collision_time: float = 10
        self.__collision_time: float = 0

        print("Debug Create Atom:", radius, color, pos, velocity, local_angle, mass, self.tolerance)

        # Vectors
        self.pos: pg.Vector2 = pg.Vector2(pos)
        self.velocity: pg.Vector2 = pg.Vector2(velocity)

    def update(self, dt):
        self.__update_collision_time(dt)

    def __update_collision_time(self, dt):
        if self.__collision_time < self.__max_collision_time:
            self.__collision_time += dt

    def update_movement(self, dt: float):
        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    def update_collision_atom(self, other: 'Atom'):
        if self.__is_collision_atom(other):
            # From Wikipedia
            print('!!!COLLISION!!!')
            print(self.velocity, other.velocity)
            self.velocity, other.velocity = self.__find_new_velocity(other), other.__find_new_velocity(self)
            print(self.velocity, other.velocity)

    # wariant - znak wielka litera, czy od North, South, etc...
    def update_collision_wall(self, container):
        if (walls := list(self.__find_collision_walls(container))) and self.is_collision_time():
            for wall in walls:
                if wall in 'NS':
                    self.velocity.y *= -1
                elif wall in 'WE':
                    self.velocity.x *= -1

    # ZDERZENIA
    # dla pary kulek sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    def is_collision_time(self):
        if self.__collision_time >= self.__max_collision_time:
            self.__collision_time = 0
            return True
        return False

    def __is_collision_atom(self, other):
        return self.pos.distance_to(other.pos) <= 2 * self.radius + self.tolerance
        # return 2 * self.radius < self.pos.distance_to(other.pos) <= 2 * self.radius + self.tolerance

    # dla pary kulka, kontener sprawdza czy było zdarzenie -> jesli tak to zwraca True i obsluguje jego mechanike
    def __find_collision_walls(self, container: AtomContainer) -> str:
        if self.pos.x + self.radius > container.border_right:
            yield 'E'
        elif self.pos.x - self.radius < container.border_left:
            yield 'W'

        if self.pos.y + self.radius > container.border_down:
            yield 'S'
        elif self.pos.y - self.radius < container.border_up:
            yield 'N'

    def __find_new_velocity(self, other: 'Atom') -> pg.Vector2:
        # v1' = v1 - (((2*m2) / (m1+m2)) * ((<v1-v2, x1-x2>) / (||x1-x2||^2)) * (x1 - x2))
        pos_diff: pg.Vector2 = self.pos - other.pos
        return self.velocity - (self.velocity - other.velocity).dot(pos_diff) / pos_diff.length_squared() * pos_diff
        # This one has mass
        # return (self.velocity
        #         - (((2 * self.mass) / (self.mass + other.mass))
        #            * (((self.velocity - other.velocity).dot(pos_diff)) / pos_diff.length_squared())
        #            * pos_diff))

    def render(self, screen: pg.Surface):
        #gfxdraw.filled_circle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.current_color)
        gfxdraw.aacircle(screen, int(self.pos.x), int(self.pos.y), int(self.radius), self.current_color)
