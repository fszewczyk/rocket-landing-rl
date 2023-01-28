_Part of [SHKYERA](https://youtu.be/Kb4bNZGqKyE) project_

![background](img/shkyera.png "Shkyera Aerospace")
![Rocket landing](img/landing_anim.gif)

# Rocket Landing - Reinforcement Learning

## Environment

I made a custom OpenAI-Gym environment with fully functioning 2D physics engine. If you want to test your own algorithms using that, download the package by simply typing in terminal:

```
pip install rocketgym
```

All the environment's functionalities are described [here](environment/README.md).

### Minimal usage

Make sure that all dependencies are installed by `pip install -r requirements.txt`

```python
from rocketgym.environment import Environment

import random

env = Environment()
observation = env.reset()
done = False

while not done:
    observation, reward, done, info = env.step(random.randint(0,3))
    env.render()
```

## Learning

```
python3 train.py -h
usage: Rocket Landing - Reinforcemeng Learning [-h] [--curriculum] [--softmax] [--save] [-model MODEL]

optional arguments:
  -h, --help    show this help message and exit
  --curriculum  Use Curriculum Learning
  --softmax     Use Softmax exploration instead of eps-greedy
  --save        Save flight logs and models every 100 episodes
  -model MODEL  Path to the model to load. Overrides the curriculum and exploration
                settings. Renders the scene from the start.
```

In the `train.py` you can see, how agent training is implemented. All you need to do is specify the exploration strategy and adjust the environment to your needs. I found that it takes around 2000 iterations to learn to land without any curriculum learning, but the process can be significantly sped up by setting up a task difficulty schedule. This can be easily done through the `Curriculum` module.

## Diagnostics

If you want to make pretty plots, like this one
![pretty plot](img/pretty_plot.png)
feel free to use `diagnostics.py`. All you need to know to do that is described in the script itself.

_**For a detailed explanation of the environment and the learning algorithms I used, see [here](url).**_
