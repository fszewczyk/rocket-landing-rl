# Rocket Landing Gym

Open AI Gym for vertical rocket landing containing an extensive tool to incorporate curriculum learning for your agents.

## Installation

```
pip install rocketgym
```

## Minimal usage

```python
from rocketgym.environment import Environment
import random

env = Environment()
observation = env.reset()
done = False

while not done:
    observation, reward, done, info = env.step(random.randint(0, 3))
    env.render()
```

## Environment

### Rocket

Rocket is treated as a 2D free body. Its physics properties have been modeled after Falcon 9. By default rocket is spawned

### State space

1. Angle made with y-axis ($rad$): [$-\frac{\pi}{2},\frac{\pi}{2}$]
2. Position Y ($m$): $[0,\infty]$
3. Velocity X ($\frac{m}{s}$): $[-\infty,\infty]$
4. Velocity Y ($\frac{m}{s}$): $[-\infty,\infty]$
5. Angular velocity ($\frac{rad}{s}$): $[-\infty,\infty]$

### Action space

At each timestep, rocket can perform one of the four actions:

1. Left - rotate the engine to the left and set maximum thrust
2. Mid - rotate the engine to the middle and set maximum thrust
3. Right - rotate the engine to the right and set maximum thrust
4. None - turn off thrust

### Reward

Reward function takes multiple components into consideration:

1. For each second, agent looses $0.3$.
2. For impact with the ground, agent receives $15$.
3. At impact, agent looses $0.5$ for each $rad$ off the vertical axis.
4. At impact, agent looses $0.25$ for each $\frac{rad}{s}$ of angular velocity
5. At impact, agent looses $1$ for each $\frac{m}{s}$ away from $-1\frac{m}{s}$ vertical velocity
6. At impact, agent looses $0.25$ for each $\frac{m}{s}$ of horizontal velocity

## Curriculum Learning

The best part about this gym. It allows you to alter the difficulty of the environment by changing things like initial height, action space etc.

### Spawn height

```python
from rocketgym.environment import Environment

env = Environment()
env.curriculum.set_fixed_height()
env.curriculum.set_random_height(1,5)

env.curriculum.enable_random_height()
env.curriculum.disable_random_height()

env.curriculum.enable_increasing_height(rate=0.05)
env.curriculum.disable_increasing_height()
```

### Spawn orientation

```python
env.curriculum.enable_random_starting_rotation()
env.curriculum.disable_random_starting_rotation()
```

### Altering the reward function

```pytohn
env.curriculum.enable_x_velocity_reward()
env.curriculum.disable_x_velocity_reward()
```
