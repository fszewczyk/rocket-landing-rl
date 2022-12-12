from dataclasses import dataclass
from queue import Queue
import math
import random
from pyquaternion import Quaternion
import numpy as np

from constants import *

import matplotlib.pyplot as plt


@dataclass
class Config():
    mass: float
    # center_of_mass: float
    # mass_moment_of_inertia: float
    delay: float
    tvc_angle_speed: float
    thrust: float
    max_angle: float
    length: float
    # noise_rotation: float
    # noise_rotation_speed: float
    # noise_speed: float
    # fuel_usage: float


def plot_3D_vec(ax, origin, vec, l=None):
    ax.plot([origin[0], origin[0]+vec[0]], [origin[1], origin[1]+vec[1]],
            [origin[2], origin[2]+vec[2]], label=l)
    return ax


class Rocket():
    def __init__(self, config):
        self.config = config
        self.__set_start_position()

    def reset(self, config=None):
        self.config = config if config is not None else self.config
        self.x

    def update(self):
        engine_movement, thrust = self.__get_actions()

        self.queued_engine_movements.put(engine_movement)
        self.queued_thrust.put(thrust)

        current_movement = self.queued_engine_movements.get()
        current_thrust = self.queued_thrust.get()

        self.engine_vector = self.__move_engine(current_movement)

        self.thrust_components = self.__get_thrust_components()
        self.__update_position()

    def plot(self, time):
        print(f"Time: {time}")
        print(f"Position: {self.x, self.y, self.z}")
        print(f"Speed {self.vx, self.vy, self.vz}")

        ax = plt.figure().add_subplot(projection='3d')
        ax = plot_3D_vec(ax, [self.x, self.y, self.z],
                         self.engine_vector, l="Engine")
        ax = plot_3D_vec(ax, [self.x, self.y, self.z],
                         self.rocket_vector, l="Rocket")
        ax = plot_3D_vec(ax, [self.x, self.y, self.z],
                         self.front_vector, l="Front")

        print(np.dot(self.thrust_components[1], self.thrust_components[2]))

        ax = plot_3D_vec(ax, [self.x, self.y, self.z],
                         self.thrust_components[1], l="Front/Back component")
        ax = plot_3D_vec(ax, [self.x, self.y, self.z],
                         self.thrust_components[2], l="Sideways component")

        ax.set(xlim=(-self.config.length + self.x, self.config.length + self.x), ylim=(-self.config.length + self.y,
               self.config.length + self.y), zlim=(self.z, self.config.length + self.z))

        ax.legend()

        plt.show()

    def __get_thrust_components(self):
        comp_along = self.rotation.rotate([self.tvc_vector[0], 0, 0])
        comp_front_back = self.rotation.rotate([0, 0, self.tvc_vector[2]])
        comp_sideways = self.rotation.rotate([0, self.tvc_vector[1], 0])

        return [comp_along, comp_front_back, comp_sideways]

    def __update_position(self):
        ax = self.thrust_components[0][0] / self.config.mass
        ay = self.thrust_components[0][1] / self.config.mass
        az = self.thrust_components[0][2] / self.config.mass - GRAVITY

        self.vx += ax * TIMESTEP
        self.vy += ay * TIMESTEP
        self.vz += az * TIMESTEP

        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP
        self.z += self.vz * TIMESTEP

    def __set_start_position(self):
        self.t = 0

        self.x = 0
        self.y = 0
        self.z = STARTING_HEIGHT

        self.vx = 0
        self.vy = 0
        self.vz = STARTING_SPEED

        self.rotation = Quaternion.random()
        self.rocket_vector = self.rotation.rotate([self.config.length, 0, 0])
        self.front_vector = self.rotation.rotate([0, 0, 1])
        self.tvc_vector = np.float32([self.config.thrust, 0, 0])
        self.engine_vector = np.float32([self.config.thrust, 0, 0])
        self.thrust_components = [
            [self.config.thrust, 0, 0], [0, 0, 0], [0, 0, 0]]

        while self.rocket_vector[2] < 0:
            self.rotation = Quaternion.random()
            self.rocket_vector = self.rotation.rotate(
                [self.config.length, 0, 0])
            self.front_vector = self.rotation.rotate([0, 0, 1])

        self.avx = 0
        self.avy = 0

        self.queued_engine_movements = Queue()
        self.queued_thrust = Queue()
        if self.config.delay / TIMESTEP > 1:
            for _ in range(int(self.config.delay / TIMESTEP)):
                self.queued_engine_movements.put(EngineMovement.STAY)
                self.queued_thrust.put(0)

        self.tvc_speed = self.config.tvc_angle_speed * TIMESTEP

    def __get_actions(self):
        return random.choice([EngineMovement.LEFT, EngineMovement.FRONT]), 1

    def __move_engine(self, movement: EngineMovement):
        if movement == EngineMovement.STAY:
            return self.rotation.rotate(self.tvc_vector)
        elif movement == EngineMovement.BACK:
            new_x = self.tvc_vector[0] * math.cos(
                self.tvc_speed) + self.tvc_vector[2] * math.sin(self.tvc_speed)
            new_z = -self.tvc_vector[0] * math.sin(
                self.tvc_speed) + self.tvc_vector[2] * math.cos(self.tvc_speed)

            dot = np.dot([self.config.thrust, 0, 0], [
                         new_x, self.tvc_vector[1], new_z])
            angle = math.acos(
                dot / (np.linalg.norm([self.config.thrust, 0, 0]) * np.linalg.norm([new_x, self.tvc_vector[1], new_z])))

            if angle < self.config.max_angle:
                self.tvc_vector[0] = new_x
                self.tvc_vector[2] = new_z

            return self.rotation.rotate(self.tvc_vector)
        elif movement == EngineMovement.FRONT:
            new_x = self.tvc_vector[0] * math.cos(
                -self.tvc_speed) + self.tvc_vector[2] * math.sin(-self.tvc_speed)
            new_z = -self.tvc_vector[0] * math.sin(
                -self.tvc_speed) + self.tvc_vector[2] * math.cos(-self.tvc_speed)

            dot = np.dot([self.config.thrust, 0, 0], [
                         new_x, self.tvc_vector[1], new_z])
            angle = math.acos(
                dot / (np.linalg.norm([self.config.thrust, 0, 0]) * np.linalg.norm([new_x, self.tvc_vector[1], new_z])))

            if angle < self.config.max_angle:
                self.tvc_vector[0] = new_x
                self.tvc_vector[2] = new_z

            return self.rotation.rotate(self.tvc_vector)

        elif movement == EngineMovement.RIGHT:
            new_x = self.tvc_vector[0] * math.cos(
                self.tvc_speed) - self.tvc_vector[1] * math.sin(self.tvc_speed)
            new_y = self.tvc_vector[0] * math.sin(
                self.tvc_speed) + self.tvc_vector[1] * math.cos(self.tvc_speed)

            dot = np.dot([self.config.thrust, 0, 0], [
                         new_x, new_y, self.tvc_vector[2]])
            angle = math.acos(
                dot / (np.linalg.norm([self.config.thrust, 0, 0]) * np.linalg.norm([
                    new_x, new_y, self.tvc_vector[2]])))

            if angle < self.config.max_angle:
                self.tvc_vector[0] = new_x
                self.tvc_vector[1] = new_y

            return self.rotation.rotate(self.tvc_vector)

        elif movement == EngineMovement.LEFT:
            new_x = self.tvc_vector[0] * math.cos(
                -self.tvc_speed) - self.tvc_vector[1] * math.sin(-self.tvc_speed)
            new_y = self.tvc_vector[0] * math.sin(
                -self.tvc_speed) + self.tvc_vector[1] * math.cos(-self.tvc_speed)

            dot = np.dot([self.config.thrust, 0, 0], [
                         new_x, new_y, self.tvc_vector[2]])
            angle = math.acos(
                dot / (np.linalg.norm([self.config.thrust, 0, 0]) * np.linalg.norm([
                    new_x, new_y, self.tvc_vector[2]])))

            if angle < self.config.max_angle:
                self.tvc_vector[0] = new_x
                self.tvc_vector[1] = new_y

            return self.rotation.rotate(self.tvc_vector)
