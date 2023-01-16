from rocket import Rocket
from tvc import TVC

from constants import *


class Environment():
    def __init__(self):
        self.reset()

    def reset(self):
        self.rocket = Rocket(STARTING_HEIGHT, WEIGHT)
        self.tvc = TVC(MAX_THRUST, THRUST_CHANGE_PER_SECOND)

        self.timestep = 0

        return self.__get_state()

    def step(self, action):
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
        return [self.rocket.y / STARTING_HEIGHT, self.rocket.velocity_y, self.tvc.current_thrust / MAX_THRUST]
