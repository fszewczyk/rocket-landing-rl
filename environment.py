from rocket import Rocket
from tvc import TVC

from constants import *


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

        self.reset()

    def reset(self):
        """!
        Resets the environment to default conditions

        @return list: current state of the environment
        """
        self.rocket = Rocket(STARTING_HEIGHT, WEIGHT)
        self.tvc = TVC(MAX_THRUST, THRUST_CHANGE_PER_SECOND,
                       ROTATION_SPEED_PER_SECOND)

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

        if engine_z_action == EngineZAction.LEFT:
            self.tvc.rotate_left()
        elif engine_z_action == EngineZAction.STAY:
            self.tvc.rotate_stay()
        elif engine_z_action == EngineZAction.RIGHT:
            self.tvc.rotate_right()

        self.rocket.update_position(self.tvc)

        reward = 0
        self.timestep += 1

        return self.__get_state(), reward, self.rocket.y <= 0 or self.rocket.y > 2*STARTING_HEIGHT

    def __get_state(self):
        """!
        Generates a vector describing the environment

        @return list: description of the environment
        """

        state = []
        state.append(self.rocket.y / STARTING_HEIGHT)
        state.append(self.rocket.velocity_y)
        state.append(self.tvc.current_thrust / MAX_THRUST)

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
