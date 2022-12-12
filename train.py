import math

from rocket import *

config = Config(mass=1, delay=0, tvc_angle_speed=math.pi,
                thrust=100, max_angle=math.pi/4, length=20)
rocket = Rocket(config)

for i in range(1000):
    rocket.update()
    if i % 100 == 0:
        rocket.plot(i * TIMESTEP)
