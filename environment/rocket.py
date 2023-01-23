import math
import cv2
import os

from .vector import Vector
from .constants import *


class FlightLog():
    def __init__(self):
        self.position_x = []
        self.position_y = []

        self.velocity_x = []
        self.velocity_y = []

        self.angular_velocity = []

        self.rocket_angle = []

        self.tvc_angle = []
        self.tvc_thrust = []

        self.time = []


class Rocket(Vector):
    """!
    Class describing the rocket.
    Note that rocket is seperate from the TVC mount.
    """

    def __init__(self, x, y, weight, moment_of_inertia, center_of_mass, dir_x=0, dir_y=1):
        """!
        Constructs the rocket object.

        @param y (float): Starting Y coordinate (height) of the rocket in 3D space.
        @param weight (float): Weight of the rocket in kg.
        """

        super(Rocket, self).__init__(x=dir_x, y=dir_y)

        self.position_x = x
        self.position_y = y

        self.velocity_x = 0
        self.velocity_y = 0

        self.angular_velocity = 0

        self.weight = weight
        self.moment_of_inertia = moment_of_inertia
        self.center_of_mass = center_of_mass

        self.flight_log = FlightLog()

        rocket_width = 250

        self.icon_idle = cv2.imread(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "img/rocket_idle.png"))
        self.icon_idle = cv2.resize(
            self.icon_idle, (rocket_width, rocket_width))

        self.icon_mid = cv2.imread(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "img/rocket_middle.png"))
        self.icon_mid = cv2.resize(self.icon_mid, (rocket_width, rocket_width))

        self.icon_right = cv2.imread(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "img/rocket_right.png"))
        self.icon_right = cv2.resize(
            self.icon_right, (rocket_width, rocket_width))

        self.icon_left = cv2.imread(os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "img/rocket_left.png"))
        self.icon_left = cv2.resize(
            self.icon_left, (rocket_width, rocket_width))

    def update_position(self, tvc):
        """!
        Updates the rocket position
        based on TVC's configuration.
        Note that this function also updates the TVC position

        @param tvc (Object): TVC object used to alter rocket's trajectory
        """

        along, side = self.get_rotated_vectors()

        # Updating rocket's position
        push_force = tvc.current_thrust * tvc.get_component_along_vector(along)
        rotate_force = tvc.current_thrust * \
            tvc.get_component_along_vector(side)

        self.velocity_x += TIMESTEP * (along.x * push_force) / self.weight

        self.velocity_y -= TIMESTEP * GRAVITY
        self.velocity_y += TIMESTEP * (along.y * push_force) / self.weight

        self.position_x += TIMESTEP * self.velocity_x
        self.position_y += TIMESTEP * self.velocity_y

        # Updating rocket's rotation
        angular_acceleration = self.center_of_mass * \
            rotate_force / self.moment_of_inertia

        angular_acceleration = round(angular_acceleration, 5)

        self.angular_velocity += TIMESTEP * angular_acceleration

        self.rotate_around_z(TIMESTEP * self.angular_velocity)
        tvc.rotate_around_z(TIMESTEP * self.angular_velocity)

    def log(self, tvc, time):
        """!
        Logs the flight data for later preview

        @param tvc (TVC): TVC object to log
        @param time (float): current timestep
        """

        self.flight_log.position_x.append(self.position_x)
        self.flight_log.position_y.append(self.position_y)

        self.flight_log.velocity_x.append(self.velocity_x)
        self.flight_log.velocity_y.append(self.velocity_y)

        self.flight_log.angular_velocity.append(
            math.degrees(self.angular_velocity))

        self.flight_log.rocket_angle.append(
            math.degrees(self.get_signed_angle_with_y_axis()))

        self.flight_log.tvc_angle.append(math.degrees(tvc.level))
        self.flight_log.tvc_thrust.append(tvc.current_thrust)

        self.flight_log.time.append(time)

    def get_unsigned_angle_with_y_axis(self):
        """!
        Calculates the unsigned angle between the rocket and the y-axis.

        @ return float: angle in radians
        """
        return abs(math.atan(self.x / self.y))

    def get_signed_angle_with_y_axis(self):
        """!
        Calculates the signed angle between the rocket and the y-axis.

        @ return float: angle in radians
        """
        return math.atan(self.x / self.y)

    def is_ground(self):
        """!
        Checks if the rocket hit the ground

        @param bool: True if rocket is on the ground
        """
        return self.position_y <= 0
