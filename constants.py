from enum import IntEnum

# Environment
STARTING_HEIGHT = 200
GRAVITY = 9.81
TIMESTEP = 0.01

# Rocket
WEIGHT = 1

# TVC
MAX_THRUST = 50
THRUST_CHANGE_PER_SECOND = 50
ROTATION_SPEED_PER_SECOND = 2


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
