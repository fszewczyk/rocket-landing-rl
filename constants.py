from enum import Enum

# Environment
STARTING_HEIGHT = 200
GRAVITY = 9.81
TIMESTEP = 0.01

# Rocket
WEIGHT = 1

# TVC
MAX_THRUST = 50
THRUST_CHANGE_PER_SECOND = 50


class ThrustAction(Enum):
    """!
    Enumeration of possible actions.
    """

    LOWER = 0
    STAY = 1
    HIGHER = 2
