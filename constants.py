from enum import Enum

STARTING_HEIGHT = 1000
STARTING_SPEED = 0

BORDER_X = 500
BORDER_Y = 500

GRAVITY = 9.81

TIMESTEP = 0.01


class EngineMovement(Enum):
    STAY = 0
    LEFT = 1
    RIGHT = 2
    FRONT = 3
    BACK = 4
