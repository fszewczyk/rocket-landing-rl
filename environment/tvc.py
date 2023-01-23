from .vector import Vector
from .constants import *


class TVC(Vector):
    """!
    Implements a thrust-vector control for the rocket.
    """

    def __init__(self, max_thrust, tvc_range, dir_x=0, dir_y=1):
        """!
        Constructs the TVC mount

        @param max_thrust (float): Maximum thrust of the engine
        @param rotation_speed (float): Speed of engine mount rotation in rad/s
        """

        super(TVC, self).__init__(x=dir_x, y=dir_y)

        self.max_thrust = max_thrust
        self.tvc_range = tvc_range

        self.current_thrust = 0

        self.level = 0

    def stay_thrust(self):
        """!
        Leaves the thrust of the engine as it is.
        """

        return

    def set_rotation_left(self):
        """!
        Sets rotation to fully left.
        """

        if self.level > 0.1:
            self.rotate_around_z(-self.tvc_range * 2)
            self.level -= self.tvc_range * 2
        elif self.level > -0.1:
            self.rotate_around_z(-self.tvc_range)
            self.level -= self.tvc_range

    def set_rotation_right(self):
        """!
        Sets rotation to fully right.
        """

        if self.level < -0.1:
            self.rotate_around_z(self.tvc_range * 2)
            self.level += self.tvc_range * 2
        elif self.level < 0.1:
            self.rotate_around_z(self.tvc_range)
            self.level += self.tvc_range

    def set_rotation_middle(self):
        """! 
        Sets rotation to middle
        """

        if self.level > 0.1:
            self.rotate_around_z(-self.tvc_range)
            self.level -= self.tvc_range
        elif self.level < -0.1:
            self.rotate_around_z(self.tvc_range)
            self.level += self.tvc_range

    def set_max_thrust(self):
        """!
        Turns on maximum thrust of the engine
        """

        self.current_thrust = self.max_thrust

    def set_min_thrust(self):
        """!
        Turns off the engine
        """

        self.current_thrust = 0

    def __str__(self):
        return f"Thrust: {self.current_thrust} N, Direction: ({self.x:.3f}, {self.y:.3f})"
