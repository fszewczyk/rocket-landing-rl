from vector import Vector
from constants import *


class TVC(Vector):
    """!
    Implements a thrust-vector control for the rocket.
    """

    def __init__(self, max_thrust, thrust_step, rotation_speed, dir_x=0, dir_y=1):
        """!
        Constructs the TVC mount

        @param max_thrust (float): Maximum thrust of the engine
        @param thrust_step (float): Rate of change of the thrust in N/s
        @param rotation_speed (float): Speed of engine mount rotation in rad/s
        """

        super(TVC, self).__init__(x=dir_x, y=dir_y)

        self.max_thrust = max_thrust
        self.thrust_step = thrust_step
        self.rotation_speed = rotation_speed

        self.current_thrust = 0

        self.level = 0

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

    # TODO: put limit on TVC rotation
    def rotate_left(self):
        """!
        Rotates the engine mount to the left around z-axis
        """

        if self.level > -MAX_ROTATION:
            self.rotate_around_z(self.rotation_speed * TIMESTEP)
            self.level -= TIMESTEP * ROTATION_SPEED_PER_SECOND

    def rotate_right(self):
        """!
        Rotates the engine mount to the left around z-axis
        """

        if self.level < MAX_ROTATION:
            self.rotate_around_z(-self.rotation_speed * TIMESTEP)
            self.level += TIMESTEP * ROTATION_SPEED_PER_SECOND

    def rotate_stay(self):
        """!
        Leaves the engine rotation as it is.
        """

        return

    def set_rotation_left(self):
        """!
        Sets rotation to fully left.
        """

        if self.level > 0.1:
            self.rotate_around_z(-MAX_ROTATION * 2)
            self.level -= MAX_ROTATION * 2
        elif self.level > -0.1:
            self.rotate_around_z(-MAX_ROTATION)
            self.level -= MAX_ROTATION

    def set_rotation_right(self):
        """!
        Sets rotation to fully right.
        """

        if self.level < -0.1:
            self.rotate_around_z(MAX_ROTATION * 2)
            self.level += MAX_ROTATION * 2
        elif self.level < 0.1:
            self.rotate_around_z(MAX_ROTATION)
            self.level += MAX_ROTATION

    def set_rotation_middle(self):
        """! 
        Sets rotation to middle
        """

        if self.level > 0.1:
            self.rotate_around_z(-MAX_ROTATION)
            self.level -= MAX_ROTATION
        elif self.level < -0.1:
            self.rotate_around_z(MAX_ROTATION)
            self.level += MAX_ROTATION

    def __str__(self):
        return f"Thrust: {self.current_thrust} N, Direction: ({self.x:.3f}, {self.y:.3f})"
