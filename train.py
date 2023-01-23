import environment.constants
from environment.constants import *
from environment.dashboard import Dashboard
import math
import matplotlib.pyplot as plt
import numpy as np
import torch

from environment.environment import Environment
from network import Agent


def train():
    dash = Dashboard()

    # Setting up the environment
    env = Environment()
    env.curriculum.enable_turn()
    env.curriculum.enable_random_starting_rotation()
    env.curriculum.enable_x_velocity_reward()

    exploration = Exploration.EPSILON_GREEDY
    exploration_dec = EPS_DECREASE
    exploration_min = EPS_MIN
    algorithm = "deepQ"

    agent = Agent(gamma=0.99, epsilon=1, lr=0.001,
                  input_dims=[5], batch_size=64, n_actions=4, exploration_dec=exploration_dec, exploration_min=exploration_min, exploration=exploration)

    scores = []
    velocities = []
    angles = []

    n_games = 2000

    for i in range(n_games):
        score = 0
        done = False

        if i == 200:  # Implementing curriculum learning
            env.curriculum.set_random_height(1, 10)
            env.curriculum.enable_increasing_height()

        observation = env.reset()

        while not done:
            action = agent.choose_action(observation)
            new_observation, reward, done, info = env.step(action)
            score += reward

            agent.store_transition(observation, action,
                                   reward, new_observation, done)
            agent.learn()

            observation = new_observation

        if i % 100 == 0:
            dash.plot_log(env.rocket.flight_log, episode=i)
            torch.save(agent.q_eval.state_dict(), f"model_{i}")

        scores.append(score)

        avg_score = np.mean(scores[-100:])

        velocity = env.rocket.flight_log.velocity_y[-1]
        if velocity < 0:
            velocities.append(velocity)
            angles.append(math.degrees(
                env.rocket.get_unsigned_angle_with_y_axis()))

        avg_vel = np.mean(velocities[-100:])
        avg_ang = np.mean(angles[-100:])

        print(
            f"Episode: {i}\n\tEpsilon: {agent.epsilon}\n\tScore: {score:.2f}\n\tAverage score: {avg_score:.4f}\n\tAverage velocity: {avg_vel:.2f}\n\tAverage angle: {avg_ang:.2f}")


if __name__ == "__main__":
    train()
