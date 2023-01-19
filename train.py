import math
import matplotlib.pyplot as plt
import numpy as np

from environment import Environment
from network import Agent
from dashboard import Dashboard
from constants import *
import constants

env = Environment()
env.curriculum.enable_turn()
env.curriculum.enable_random_starting_rotation()

agent = Agent(gamma=0.95, epsilon=1.0, lr=0.001,
              input_dims=[6], batch_size=64, n_actions=4, eps_dec=EPS_DECREASE)

scores = []
velocities = []
angles = []

n_games = 100000

dash = Dashboard()
env.curriculum.set_random_height(1, 2)
env.curriculum.enable_random_height()

for i in range(n_games):
    score = 0
    done = False

    observation = env.reset()

    if i == 500:
        env.curriculum.set_random_height(0.5, 2.5)
        env.curriculum.enable_random_height()
        agent.epsilon = 0.1

    if i == 1000:
        env.curriculum.set_random_height(1.5, 10)
        agent.epsilon = 0.1

    if i == 2000:
        agent.epsilon = 0.1
        env.curriculum.set_random_height(2, 20)

    if i == 2500:
        agent.epsilon = 0.1
        env.curriculum.enable_x_velocity_reward()

    if i == 3500:
        agent.epsilon = 0.2
        env.curriculum.enable_landing_target()

    while not done:
        action = agent.choose_action(observation)
        new_observation, reward, done = env.step(action, i)
        score += reward

        agent.store_transition(observation, action,
                               reward, new_observation, done)
        agent.learn()

        observation = new_observation

        if i >= 5000:
            env.render()

    if i % 100 == 0:
        dash.plot_log(env.rocket.flight_log, episode=i)

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
        f"Episode: {i}\n\tEpsilon: {agent.epsilon}\n\tScore: {score:.2f}\n\tAverage score: {avg_score:.4f}\n\tAverage velocity: {avg_vel:.2f}\n\tAverage angle: {avg_ang:.2f}\n\tImpact velocity: {velocity:.2f}\n\tImpact direction:{env.rocket}\n\tTotal time: {len(env.rocket.flight_log.time) * TIMESTEP :.2f}")

observation = env.reset()
done = False

while not done:
    action = agent.choose_action(observation)
    new_observation, reward, done = env.step(action, n_games)
    score += reward

    # agent.store_transition(observation, action,
    #                        reward, new_observation, done)
    # agent.learn()

    observation = new_observation

log = env.rocket.flight_log


# plt.axis('equal')
# plt.scatter(log.position_x, log.position_y, label="Trajectory")
# plt.show()

# plt.plot(log.tvc_thrust, label="Thrust")
# plt.show()

# plt.plot(log.tvc_angle, label="Angle")
# plt.show()

# plt.plot(log.angular_velocity, label="Angular velocity")
# plt.show()
