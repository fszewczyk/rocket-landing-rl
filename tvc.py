from vector import Vector
from constants import *


class TVC(Vector):
    """ Implements a thrust-vector control for the rocket.
    """

    def __init__(self, max_thrust, thrust_step):
        """ Constructs the TVC mount

        Args:
            max_thrust (float): Maximum thrust of the engine
            thrust_step (float): Rate of change of the thrust in N/s
        """

        super().__init__(1)

        self.max_thrust = max_thrust
        self.thrust_step = thrust_step
        self.current_thrust = 0

    def increase_thrust(self):
        """ Increases the thrust of the engine.
        """

        self.current_thrust = min(
            self.current_thrust + (self.thrust_step * TIMESTEP), self.max_thrust)

    def decrease_thrust(self):
        """ Decreases the thrust of the engine.
        """

        self.current_thrust = max(
            0, self.current_thrust - (self.thrust_step * TIMESTEP))

    def stay_thrust(self):
        """ Leaves the thrust of the engine as it is.
        """

        return
