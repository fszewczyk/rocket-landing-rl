from vector import Vector

from constants import *


class Rocket(Vector):
    def __init__(self, y, weight):
        super().__init__(1)

        self.y = y
        self.weight = weight

        self.velocity_y = 0

    def update_position(self, tvc):
        self.velocity_y -= TIMESTEP * GRAVITY
        self.velocity_y += TIMESTEP * (tvc.current_thrust / self.weight)

        self.y += TIMESTEP * self.velocity_y
