from vector import Vector

from constants import *


class Rocket(Vector):
    """ Class describing the rocket. 
        Note that rocket is seperate from the TVC mount.
    """

    def __init__(self, y, weight):
        """Constructs the rocket object.

        Args:
            y (float): Starting Y coordinate (height) of the rocket in 3D space.
            weight (float): Weight of the rocket in kg.
        """
        super().__init__(1)

        self.y = y
        self.weight = weight

        self.velocity_y = 0

    def update_position(self, tvc):
        """ Updates the rocket position 
            based on TVC's configuration.

        Args:
            tvc (Object): TVC object used to alter rocket's trajectory
        """

        self.velocity_y -= TIMESTEP * GRAVITY
        self.velocity_y += TIMESTEP * (tvc.current_thrust / self.weight)

        self.y += TIMESTEP * self.velocity_y
