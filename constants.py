from enum import IntEnum

# Environment
STARTING_HEIGHT = 10
GRAVITY = 9.81
TIMESTEP = 0.035

# Rocket
WEIGHT = 1
CENTER_OF_MASS = 0.5
MOMENT_OF_INERTIA = 0.1

# TVC
MAX_THRUST = 16.5
THRUST_CHANGE_PER_SECOND = 20
ROTATION_SPEED_PER_SECOND = 0.06
MAX_ROTATION = 0.15

# Rewards
PENALTY_PER_SECOND = 1
PENALTY_PER_SECOND_GOING_UP = 10
PENALTY_PER_RADIAN_OFF_PER_SECOND = 10
PENALTY_PER_RADIAN_AT_LANDING = 5

PENALTY_PER_M_S_AT_LANDING = 0.02
PENALTY_PER_METER_OF_TARGET = 1

REWARD_LANDED = 10

# Curriculum
EPS_DECREASE = 2e-4
EPS_RESTART = 0.65


class Action(IntEnum):
    """!
    Enumeration of possible actions.
    Pattern: THRUST_DIRECTION
    """

    LOWER_LEFT = 0
    STAY_LEFT = 1
    HIGHER_LEFT = 2

    LOWER_STAY = 3
    STAY_STAY = 4
    HIGHER_STAY = 5

    LOWER_RIGHT = 6
    STAY_RIGHT = 7
    HIGHER_RIGHT = 8


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
