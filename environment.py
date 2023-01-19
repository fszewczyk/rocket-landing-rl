import math
import random

from rocket import Rocket
from tvc import TVC
from constants import *

import gym


class Curriculum():
    """!
    Used for Curriculum Learning.
    Defines the current settings of the environment.
    """

    def __init__(self):
        """!
        Initializes the curriculum.
        By default:
            a) turning is disabled
            b) rocket starts from a fixed height
            c) rocket starts in an upright position
        """

        self.set_fixed_height()
        self.disable_turn()
        self.disable_random_starting_rotation()
        self.disable_random_height()
        self.disable_x_velocity_reward()
        self.disable_landing_target()

    def set_fixed_height(self):
        """!
        Sets the starting height of the rocket to a fixed number
        """
        self.start_height = STARTING_HEIGHT

    def set_random_height(self, mi, ma):
        """!
        Sets the starting height of the rocket to a fixed number
        """
        self.start_height = STARTING_HEIGHT

        self.min = mi
        self.max = ma

    def disable_random_height(self):
        self.fixed_height = True

    def enable_random_height(self):
        self.fixed_height = False

    def get_height(self):
        if self.fixed_height:
            return self.start_height
        else:
            return random.uniform(self.min, self.max)

    def disable_x_velocity_reward(self):
        self.x_velocity_reward = False

    def enable_x_velocity_reward(self):
        self.x_velocity_reward = True

    def disable_turn(self):
        """!
        Disables rocket's ability to turn the TVC engine
        """
        self.allow_turn = False

    def enable_turn(self):
        """!
        Enables rocket's ability to turn the TVC engine
        """
        self.allow_turn = True

    def enable_random_starting_rotation(self):
        """!
        Enables random starting rotation of a rocket
        """
        self.random_rotation = True

    def disable_random_starting_rotation(self):
        """!
        Disables random starting rotation of a rocket
        """
        self.random_rotation = False

    def enable_landing_target(self):
        self.land_at_target = True

    def disable_landing_target(self):
        self.land_at_target = False


class Environment(gym.Env):
    """!
    Class describing the environment.
    Contains the rocket and the engine mount.
    All the interaction with the environment should happen
    through this module.
    """

    def __init__(self):
        """!
        Constructs the environment.
        """

        super(Environment, self).__init__()

        self.observation_shape = (1000, 400, 3)
        self.observation_space = spaces.Box(low=np.zeros(self.observation_shape),
                                            high=np.ones(
                                                self.observation_shape),
                                            dtype=np.float16)

        self.action_space = spaces.Discrete(4,)

        self.canvas = np.ones(self.observation_shape) * 1

        self.curriculum = Curriculum()
        self.reset()

    def reset(self):
        """!
        Resets the environment to conditions defined
        by curriculum and predefined constants

        @return list: current state of the environment
        """

        start_dx = 0
        start_dy = 1
        if self.curriculum.random_rotation:
            start_dx = random.uniform(-0.5, 0.5)
            start_dy = random.uniform(0.5, 1)

        start_position = 0
        if self.curriculum.land_at_target:
            start_position = random.uniform(-3, 3)

        self.rocket = Rocket(start_position, self.curriculum.get_height(), WEIGHT,
                             MOMENT_OF_INERTIA, CENTER_OF_MASS, dir_x=start_dx, dir_y=start_dy)
        self.tvc = TVC(MAX_THRUST, THRUST_CHANGE_PER_SECOND,
                       ROTATION_SPEED_PER_SECOND, dir_x=start_dx, dir_y=start_dy)

        self.timestep = 0

        return self.__get_state()

    def step(self, action, it):
        """!
        Updates the environment for one timestep.

        @param action (Action): _description_

        @return list: newly observed state of the environment
        @return float: sampled reward
        @return boolean: whether or not the simulation is finished
        """

        if action == Action.LEFT:
            self.tvc.set_rotation_left()
            self.tvc.current_thrust = MAX_THRUST
        elif action == Action.MIDDLE:
            self.tvc.set_rotation_middle()
            self.tvc.current_thrust = MAX_THRUST
        elif action == Action.RIGHT:
            self.tvc.set_rotation_right()
            self.tvc.current_thrust = MAX_THRUST
        else:
            self.tvc.current_thrust = 0

        # print(action, self.tvc.current_thrust, self.tvc.level)

        self.rocket.update_position(self.tvc)
        self.rocket.log(self.tvc, self.timestep)

        reward = 0
        reward -= 0.0001

        if self.rocket.position_y <= 0:
            reward = 6 + self.rocket.velocity_y - \
                self.rocket.get_unsigned_angle_with_y_axis() - \
                0.2*abs(self.rocket.angular_velocity)

            if self.curriculum.x_velocity_reward:
                reward -= 0.5 * abs(self.rocket.velocity_x)

            if self.curriculum.land_at_target:
                reward -= 0.3 * abs(self.rocket.position_x)

        self.timestep += TIMESTEP

        return self.__get_state(), reward, self.rocket.position_y <= 0 or abs(self.rocket.position_x) > 5 or self.rocket.y < 0

    def __get_state(self):
        """!
        Generates a vector describing the environment

        @return list: description of the environment
        """

        state = []
        state.append(STARTING_HEIGHT - self.rocket.position_y)
        state.append(self.rocket.velocity_y)
        state.append(self.rocket.velocity_x)
        state.append(self.rocket.position_x)
        state.append(self.rocket.angular_velocity)
        state.append(self.rocket.get_signed_angle_with_y_axis())

        return state

    def __str__(self):
        along, side = self.rocket.get_rotated_vectors()
        return f"Environment:\n\tRocket: {self.rocket}\n\tTVC: {self.tvc}\n\tImpact on rocket: \n\t\tPush: {self.tvc.current_thrust * self.tvc.get_component_along_vector(along):.2f} N\n\t\tRotate: {self.tvc.current_thrust * self.tvc.get_component_along_vector(side):.2f} N"
