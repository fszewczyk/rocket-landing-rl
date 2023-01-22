from enum import IntEnum

# Environment
STARTING_HEIGHT = 1
GRAVITY = 9.81
TIMESTEP = 0.02

# Rocket
WEIGHT = 4.5e5
CENTER_OF_MASS = 16
MOMENT_OF_INERTIA = 2.15e6

# TVC
MAX_THRUST = 7.6e6
MAX_ROTATION = 0.2

# Reward
REWARD_LANDING = 15
PENALTY_PER_SECOND = 0.3
PENALTY_PER_RADIAN_AT_LANDING = 0.5
PENALTY_PER_ANGULAR_VELOCITY_AT_LANDING = 0.25
PENALTY_PER_HORIZONTAL_VELOCITY = 0.25
PENALTY_PER_HORIZONTAL_POSITION = 0.05

# Curriculum
EPS_DECREASE = 5e-5
EPS_RESTART = 0.65
EPS_MIN = 0.01

TEMP_DECREASE = 5e-5
TEMP_MIN = 0.004


class Action(IntEnum):
    """!
    Enumeration of possible actions.
    Pattern: THRUST_DIRECTION
    """

    LEFT = 0
    MIDDLE = 1
    RIGHT = 2
    NOTHING = 3


class Exploration(IntEnum):
    """!
    Enumeration of possible exploration strategies.
    """

    EPSILON_GREEDY = 0
    SOFTMAX = 1
