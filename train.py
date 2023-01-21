import math
import matplotlib.pyplot as plt
import numpy as np
import torch

from environment import Environment
from network import Agent
from dashboard import Dashboard
from constants import *
import constants

env = Environment()
env.curriculum.enable_turn()
env.curriculum.enable_random_starting_rotation()

lr = 0.004
agent = Agent(gamma=0.99, epsilon=0.1, lr=lr,
              input_dims=[5], batch_size=64, n_actions=4, eps_dec=TEMP_DECREASE, eps_min=0.01, exploration=Exploration.EPSILON_GREEDY)


scores = []
velocities = []
angles = []

n_games = 100000

dash = Dashboard()

agent.q_eval.load_state_dict(torch.load("models/model_1800"))
env.curriculum.set_random_height(1, 10)
env.curriculum.enable_increasing_height()

for i in range(n_games):
    score = 0
    done = False

    observation = env.reset()

    if i == 250:
        env.curriculum.set_random_height(1, 10)
        env.curriculum.enable_increasing_height()

    if i == 1000:
        agent.epsilon = 0.2
        env.curriculum.enable_x_velocity_reward()

    while not done:
        action = agent.choose_action(observation)
        new_observation, reward, done = env.step(action, i)
        score += reward

        agent.store_transition(observation, action,
                               reward, new_observation, done)
        # agent.learn()

        observation = new_observation

        env.render()

    if i % 100 == 0:
        dash.plot_log(env.rocket.flight_log, episode=i)
        torch.save(agent.q_eval.state_dict(), f"models/model_{i}")

        agent.q_eval.optimizer.param_groups[0]["lr"] = lr
        lr *= 0.9

    scores.append(score)

    avg_score = np.mean(scores[-100:])

    velocity = env.rocket.flight_log.velocity_y[-1]
    if velocity > 0:
        print("Failed")
    else:
        velocities.append(velocity)
        angles.append(math.degrees(
            env.rocket.get_unsigned_angle_with_y_axis()))

    avg_vel = np.mean(velocities[-100:])
    avg_ang = np.mean(angles[-100:])

    print(
        f"Episode: {i}\n\tEpsilon: {agent.epsilon}\n\tScore: {score:.2f}\n\tAverage score: {avg_score:.4f}\n\tAverage velocity: {avg_vel:.2f}\n\tAverage angle: {avg_ang:.2f}")
