from rocket import Rocket
from tvc import TVC

from constants import *


class Environment():
    """ Class describing the environment. 
        Contains the rocket and the engine mount.
        All the interaction with the environment should happen 
        through this module. 
    """

    def __init__(self):
        """Constructs the environment.
        """

        self.reset()

    def reset(self):
        """ Resets the environment to default conditions

        Returns:
            list: current state of the environment
        """
        self.rocket = Rocket(STARTING_HEIGHT, WEIGHT)
        self.tvc = TVC(MAX_THRUST, THRUST_CHANGE_PER_SECOND)

        self.timestep = 0

        return self.__get_state()

    def step(self, action):
        """ Updates the environment for one timestep.

        Args:
            action (ThrustAction): _description_

        Returns:
            list: newly observed state of the environment
            float: sampled reward
            boolean: whether or not the simulation is finished
        """

        if action == ThrustAction.LOWER:
            self.tvc.decrease_thrust()
        elif action == ThrustAction.STAY:
            self.tvc.stay_thrust()
        elif action == ThrustAction.HIGHER:
            self.tvc.increase_thrust()

        self.rocket.update_position(self.tvc)

        reward = 0
        self.timestep += 1

        return self.__get_state(), reward, self.rocket.y <= 0 or self.rocket.y > 2*STARTING_HEIGHT

    def __get_state(self):
        """ Generates a vector describing the environment

        Returns:
            list: description of the environment
        """

        state = []
        state.append(self.rocket.y / STARTING_HEIGHT)
        state.append(self.rocket.velocity_y)
        state.append(self.tvc.current_thrust / MAX_THRUST)

        return state
