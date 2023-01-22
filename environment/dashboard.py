import matplotlib.pyplot as plt
import matplotlib
import os
import pandas as pd
import numpy as np
import math


class Dashboard():
    """!
    Dashboard module taking care of data visualization
    """

    def __init__(self, fn=None):
        super().__init__()

        self.fn = fn

    def plot_log(self, log, episode=None):
        """!
        Generates and saves a dashboard of a given flight.

        @param log (FlightLog): Flight's log
        @param episode (int): Episode number
        """
        fig = plt.figure(figsize=(12, 12))
        grid = plt.GridSpec(3, 2, hspace=0.35, wspace=0.35)

        tl = fig.add_subplot(grid[0, 0])
        tr = fig.add_subplot(grid[0, 1])
        cl = fig.add_subplot(grid[1, 0])
        cr = fig.add_subplot(grid[1, 1])
        bl = fig.add_subplot(grid[2, 0])
        br = fig.add_subplot(grid[2, 1])
        # TODO: set figure title

        tl.set_title("Trajectory")
        tl.scatter(log.position_x[::2],
                   log.position_y[::2])
        tl.set_xlabel("Position X (m)")
        tl.set_ylabel("Position Y (m)")
        tl.axis('equal')

        tr.set_title("Position")
        tr.plot(log.time, log.position_x, label="Position X")
        tr.plot(log.time, log.position_y, label="Position Y")
        tr.legend()
        tr.set_xlabel("Time (s)")
        tr.set_ylabel("Position (m)")

        cl.set_title("Rocket and TVC orientation")
        cl.plot(log.time, log.rocket_angle, label="Rocket angle")
        cl.plot(log.time, log.tvc_angle, label="TVC angle")
        cl.legend()
        cl.set_xlabel("Time (s)")
        cl.set_ylabel("Rotation (deg)")

        cr.set_title("Rocket angular speed")
        cr.plot(log.time, log.angular_velocity)
        cr.set_xlabel("Time (s)")
        cr.set_ylabel("Angular speed (deg/s)")

        bl.set_title("Rocket velocity")
        bl.plot(log.time, log.velocity_x, label="Horizontal velocity")
        bl.plot(log.time, log.velocity_y, label="Vertical velocity")
        bl.legend()
        bl.set_xlabel("Time(s)")
        bl.set_ylabel("Velocity (m/s)")

        br.set_title("Thrust")
        br.plot(log.time, log.tvc_thrust)
        br.set_xlabel("Time (s)")
        br.set_ylabel("Thrust (N)")

        plt.savefig(f'logs/plots/flight_{episode}.png', dpi=200)

    def write_header_to_file(self, string):
        with open(os.path.join("logs", "data", self.fn), 'w') as f:
            f.write(f"{string}\n")
            f.close()

    def write_record_to_file(self, args):
        with open(os.path.join("logs", "data", self.fn), 'a') as f:
            for i, arg in enumerate(args):
                if i < len(args) - 1:
                    f.write(f"{arg},")
                else:
                    f.write(f"{arg}\n")

            f.close()

    def plot_rewards(self, dirs):
        plt.plot([200, 200], [-4, 15], color=(0, 0, 0, 0.5))
        plt.plot([1100, 1100], [-4, 15], color=(0, 0, 0, 0.5))
        plt.xlim((0, 2000))
        plt.ylim((-3, 14))
        plt.xlabel("Episode")
        plt.ylabel("Average reward")

        for i, d in enumerate(dirs):
            perf = []
            episodes = []
            for f in os.listdir(d):
                data = pd.read_csv(os.path.join(d, f))

                scores = data['score'].tolist()
                episodes = data['episode'].tolist()
                algo = data['algorithm'].tolist()
                expl = data['exploration_strategy'].tolist()

                scores = np.convolve(
                    scores, np.ones(20)/20, mode='valid')

                if len(scores) > 1900:
                    perf.append(scores)

            err = np.std(perf, axis=0)  # / math.sqrt(len(os.listdir(d)))
            p = plt.plot(range(len(perf[0])), np.mean(
                perf, axis=0), label=d[10:], linewidth=3)
            plt.fill_between(range(len(perf[0])), np.mean(
                perf, axis=0) + err, np.mean(perf, axis=0) - err, alpha=0.25, color=p[0].get_color())

        plt.legend()
        plt.show()
