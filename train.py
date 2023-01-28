import environment.constants
from environment.constants import *
from environment.dashboard import Dashboard
import math
import matplotlib.pyplot as plt
import numpy as np
import torch
import argparse

from environment.environment import Environment
from network import Agent


def train(curriculum, softmax, save_progress, model=None):
    dash = Dashboard()

    # Setting up the environment
    env = Environment()
    env.curriculum.enable_turn()
    env.curriculum.enable_random_starting_rotation()
    env.curriculum.enable_x_velocity_reward()

    if not curriculum:
        env.curriculum.set_random_height(1, 10)
        env.curriculum.enable_increasing_height()

    if softmax:
        exploration = Exploration.SOFTMAX
        exploration_dec = TEMP_DECREASE
        exploration_min = TEMP_MIN
        exploration_start = TEMP_START
    else:
        exploration = Exploration.EPSILON_GREEDY
        exploration_dec = EPS_DECREASE
        exploration_min = EPS_MIN
        exploration_start = EPS_START

    algorithm = "deepQ"

    if model is None:
        agent = Agent(gamma=0.99, epsilon=exploration_start, lr=0.001,
                      input_dims=[5], batch_size=64, n_actions=4, exploration_dec=exploration_dec, exploration_min=exploration_min, exploration=exploration)
    else:
        agent = Agent(gamma=0.99, epsilon=0, lr=0.001,
                      input_dims=[5], batch_size=64, n_actions=4, exploration_dec=exploration_dec, exploration_min=exploration_min, exploration=exploration)
        agent.q_eval.load_state_dict(torch.load(model))

        env.curriculum.set_random_height(1, 10)
        env.curriculum.enable_increasing_height()

    scores = []
    velocities = []
    angles = []

    n_games = 2000

    for i in range(n_games):
        score = 0
        done = False

        if curriculum and i == 200:
            env.curriculum.set_random_height(1, 1)
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

            if model is not None or i >= 1950:
                env.render()

        if save_progress and i % 100 == 0:
            dash.plot_log(env.rocket.flight_log, episode=i)
            torch.save(agent.q_eval.state_dict(),
                       f"models/model_{i}")

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
    parser = argparse.ArgumentParser(
        prog='Rocket Landing - Reinforcemeng Learning')

    parser.add_argument('--curriculum', action='store_true',
                        help="Use Curriculum Learning")
    parser.add_argument('--softmax', action='store_true',
                        help="Use Softmax exploration instead of eps-greedy")
    parser.add_argument('--save', action='store_true',
                        help="Save flight logs and models every 100 episodes")
    parser.add_argument('-model',
                        help="Path to the model to load. Overrides the curriculum and exploration settings. Renders the scene from the start.")

    args = parser.parse_args()

    train(args.curriculum, args.softmax, args.save, args.model)
