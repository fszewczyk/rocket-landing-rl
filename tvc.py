from vector import Vector
from constants import *


class TVC(Vector):
    """!
    Implements a thrust-vector control for the rocket.
    """

    def __init__(self, max_thrust, thrust_step, rotation_speed):
        """!
        Constructs the TVC mount

        @param max_thrust (float): Maximum thrust of the engine
        @param thrust_step (float): Rate of change of the thrust in N/s
        @param rotation_speed (float): Speed of engine mount rotation in rad/s
        """

        super(TVC, self).__init__()

        self.max_thrust = max_thrust
        self.thrust_step = thrust_step
        self.rotation_speed = rotation_speed

        self.current_thrust = 0

    def increase_thrust(self):
        """!
        Increases the thrust of the engine.
        """

        self.current_thrust = min(
            self.current_thrust + (self.thrust_step * TIMESTEP), self.max_thrust)

    def decrease_thrust(self):
        """!
        Decreases the thrust of the engine.
        """

        self.current_thrust = max(
            0, self.current_thrust - (self.thrust_step * TIMESTEP))

    def stay_thrust(self):
        """!
        Leaves the thrust of the engine as it is.
        """

        return

    def rotate_left(self):
        """!
        Rotates the engine mount to the left around z-axis
        """

        self.rotate_around_z(self.rotation_speed * TIMESTEP)

    def rotate_right(self):
        """!
        Rotates the engine mount to the left around z-axis
        """

        self.rotate_around_z(-self.rotation_speed * TIMESTEP)

    def rotate_stay(self):
        """!
        Leaves the engine rotation as it is.
        """

        return
