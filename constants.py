from enum import IntEnum

# Environment
STARTING_HEIGHT = 1.4
GRAVITY = 9.81
TIMESTEP = 0.035

# Rocket
WEIGHT = 1
CENTER_OF_MASS = 0.5
MOMENT_OF_INERTIA = 0.3

# TVC
MAX_THRUST = 15.5
THRUST_CHANGE_PER_SECOND = 20
ROTATION_SPEED_PER_SECOND = 0.06
MAX_ROTATION = 0.15

# Rewards
PENALTY_PER_SECOND = 1
PENALTY_PER_SECOND_GOING_UP = 10
PENALTY_PER_RADIAN_OFF_PER_SECOND = 10
PENALTY_PER_RADIAN_AT_LANDING = 1.5
PENALTY_PER_ANGULAR_SPEED_AT_LANDING = 0.1

PENALTY_PER_M_S_AT_LANDING = 1
PENALTY_PER_METER_OF_TARGET = 1

REWARD_LANDED = 10

# Curriculum
EPS_DECREASE = 1e-4
EPS_RESTART = 0.65


class Action(IntEnum):
    """!
    Enumeration of possible actions.
    Pattern: THRUST_DIRECTION
    """

    LEFT = 0
    MIDDLE = 1
    RIGHT = 2
    NOTHING = 3


class ThrustAction(IntEnum):
    """!
    Enumeration of possible thrust actions.
    """

    LOWER = 0
    STAY = 1
    HIGHER = 2


class EngineZAction(IntEnum):
    """!
    Enumeration of possible engine mount actions in z-axis.
    """

    LEFT = 0
    STAY = 1
    RIGHT = 2
