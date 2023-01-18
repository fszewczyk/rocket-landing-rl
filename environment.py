import math
import random

from rocket import Rocket
from tvc import TVC
from constants import *


class Curriculum():
    def __init__(self):
        self.set_fixed_height()
        self.disable_turn()
        self.disable_random_starting_rotation()

    def set_fixed_height(self):
        self.start_height = STARTING_HEIGHT

    def disable_turn(self):
        self.allow_turn = False

    def enable_turn(self):
        self.allow_turn = True

    def enable_random_starting_rotation(self):
        self.random_rotation = True

    def disable_random_starting_rotation(self):
        self.random_rotation = False


class Environment():
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
        self.curriculum = Curriculum()
        self.reset()

    def reset(self):
        """!
        Resets the environment to default conditions

        @return list: current state of the environment
        """
        start_dx = 0
        start_dy = 1
        if self.curriculum.random_rotation:
            start_dx = random.uniform(-0.5, 0.5)
            start_dy = random.uniform(0.5, 1)

        self.rocket = Rocket(0, self.curriculum.start_height, WEIGHT,
                             MOMENT_OF_INERTIA, CENTER_OF_MASS, dir_x=start_dx, dir_y=start_dy)
        self.tvc = TVC(MAX_THRUST, THRUST_CHANGE_PER_SECOND,
                       ROTATION_SPEED_PER_SECOND, dir_x=start_dx, dir_y=start_dy)

        self.timestep = 0

        return self.__get_state()

    def step(self, action):
        """!
        Updates the environment for one timestep.

        @param action (Action): _description_

        @return list: newly observed state of the environment
        @return float: sampled reward
        @return boolean: whether or not the simulation is finished
        """

        thrust_action = self.__get_thrust_action(action)
        engine_z_action = self.__get_engine_z_action(action)

        if thrust_action == ThrustAction.LOWER:
            self.tvc.decrease_thrust()
        elif thrust_action == ThrustAction.STAY:
            self.tvc.stay_thrust()
        elif thrust_action == ThrustAction.HIGHER:
            self.tvc.increase_thrust()

        if self.curriculum.allow_turn and engine_z_action == EngineZAction.LEFT:
            self.tvc.rotate_left()
        elif self.curriculum.allow_turn and engine_z_action == EngineZAction.STAY:
            self.tvc.rotate_stay()
        elif self.curriculum.allow_turn and engine_z_action == EngineZAction.RIGHT:
            self.tvc.rotate_right()

        self.rocket.update_position(self.tvc)
        self.rocket.log(self.tvc)

        reward = 0

        if self.rocket.position_y <= 0:
            reward += REWARD_LANDED
            reward -= PENALTY_PER_M_S_AT_LANDING * (self.rocket.velocity_y**2)
            reward -= PENALTY_PER_RADIAN_AT_LANDING * \
                abs(math.atan(self.rocket.x / self.rocket.y))

        reward -= TIMESTEP * PENALTY_PER_RADIAN_OFF_PER_SECOND * \
            abs(math.atan(self.rocket.x / self.rocket.y))

        self.timestep += 1

        return self.__get_state(), reward, self.rocket.position_y <= 0 or self.rocket.position_y > 2*STARTING_HEIGHT or self.rocket.y < 0

    def __get_state(self):
        """!
        Generates a vector describing the environment

        @return list: description of the environment
        """

        state = []
        state.append(self.rocket.position_y / STARTING_HEIGHT)
        state.append(self.rocket.position_x)
        state.append(self.rocket.velocity_y)
        state.append(self.rocket.velocity_x)
        state.append(self.rocket.angular_velocity)
        state.append(self.rocket.x)
        state.append(self.rocket.y)
        state.append(self.tvc.level)
        state.append(self.tvc.current_thrust)

        return state

    def __get_thrust_action(self, action):
        """!
        Extracts the ThrustAction from a general Action.

        @param action (Action): General action to take

        @return ThrustAction: Thrust action
        """

        if action % 3 == 0:
            return ThrustAction.LOWER
        elif action % 3 == 1:
            return ThrustAction.STAY
        elif action % 3 == 2:
            return ThrustAction.HIGHER

    def __get_engine_z_action(self, action):
        """!
        Extracts the EngienZAction from a general Action.

        @param action (Action): General action to take

        @return EngineZAction: Action of the Engine in z-axis
        """

        if action < 3:
            return EngineZAction.LEFT
        elif action < 6:
            return EngineZAction.STAY
        elif action < 9:
            return EngineZAction.RIGHT

    def __str__(self):
        along, side = self.rocket.get_rotated_vectors()
        return f"Environment:\n\tRocket: {self.rocket}\n\tTVC: {self.tvc}\n\tImpact on rocket: \n\t\tPush: {self.tvc.current_thrust * self.tvc.get_component_along_vector(along):.2f} N\n\t\tRotate: {self.tvc.current_thrust * self.tvc.get_component_along_vector(side):.2f} N"
