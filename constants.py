from enum import IntEnum

# Environment
STARTING_HEIGHT = 1
GRAVITY = 9.81
TIMESTEP = 0.02

# Rocket
WEIGHT = 5.5e5
CENTER_OF_MASS = 11
MOMENT_OF_INERTIA = 2.15e6

# TVC
MAX_THRUST = 7.6e6
ROTATION_SPEED_PER_SECOND = 0.06
MAX_ROTATION = 0.15

# Reward
REWARD_LANDING = 10
PENALTY_PER_SECOND = 0.5
PENALTY_PER_RADIAN_AT_LANDING = 1
PENALTY_PER_ANGULAR_VELOCITY_AT_LANDING = 0.2
PENALTY_PER_HORIZONTAL_VELOCITY = 0.5
PENALTY_PER_HORIZONTAL_POSITION = 0.05

# Curriculum
EPS_DECREASE = 1e-4
EPS_RESTART = 0.65

TEMP_DECREASE = 1e-4


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
