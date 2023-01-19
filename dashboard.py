import matplotlib.pyplot as plt
import matplotlib


class Dashboard():
    """!
    Dashboard module taking care of data visualization
    """

    def __init__(self):
        super().__init__()

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

        plt.savefig(f'logs/flight_{episode}.png', dpi=200)
