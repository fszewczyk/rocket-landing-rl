_Part of [SHKYERA](https://youtu.be/Kb4bNZGqKyE) project_

## _Still in development_

![background](icons/shkyera.png "Shkyera Aerospace")
![Rocket landing](icons/landing_anim.gif)

# Rocket Landing - Reinforcement Learning

## Environment

I made a custom OpenAI-Gym environment with fully functioning 2D physics engine. If you want to test your own algorithms using that, download the package by simply typing in terminal (not yet :))

```
pip install rocket-landing-gym
```

All the environment's functionalities are described [here](url).

### Minimal usage

```python
from rocketgym import Environment

env = Environment()
agent = Agent(gamma=0.99, epsilon=1, lr=0.001,
                  input_dims=[5], batch_size=64)

observation = env.reset()
done = False

while not done:
    action = agent.choose_action(observation)
    new_observation, reward, done = env.step(action)
    observation = new_observation
    env.render()
```

## Learning

In the `train.py` you can see, how agent training is implemented. All you need to do is specify the exploration strategy and adjust the environment to your needs. More info about adjusting the environment and learning process is [here](url). I found that it takes around 2000 iterations to learn to land without any curriculum learning, but the process can be significantly sped up by setting up a task difficulty schedule. This can be easily done through the `Curriculum` module.

## Diagnostics

If you want to make pretty plots, like this one
![pretty plot](icons/pretty_plot.png)
feel free to use `diagnostics.py`. All you need to know to do that is described in the script itself.
