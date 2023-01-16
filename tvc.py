from vector import Vector
from constants import *


class TVC(Vector):
    def __init__(self, max_thrust, thrust_step):
        super().__init__(1)

        self.max_thrust = max_thrust
        self.thrust_step = thrust_step
        self.current_thrust = 0

    def increase_thrust(self):
        self.current_thrust = min(
            self.current_thrust + (self.thrust_step * TIMESTEP), self.max_thrust)

    def decrease_thrust(self):
        self.current_thrust = max(
            0, self.current_thrust - (self.thrust_step * TIMESTEP))

    def stay_thrust(self):
        return
