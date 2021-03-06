from math import atan
import numpy as numpy
from pid import PID
from lowpass import LowPassFilter

class YawController(object):
    def __init__(self, wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle):
        self.wheel_base = wheel_base
        self.steer_ratio = steer_ratio
        self.min_speed = min_speed
        self.max_lat_accel = max_lat_accel

        self.min_angle = -max_steer_angle
        self.max_angle = max_steer_angle
        self.linear_pid = PID(0.9, 0.001, 0.0004, self.min_angle, self.max_angle)
        self.cte_pid = PID(0.85, 0, 0.22, self.min_angle, self.max_angle)
        self.tau = 0.2
        self.ts = 0.1
        self.lpf = LowPassFilter(self.tau, self.ts)

    def get_angle(self, radius):
        angle = atan(self.wheel_base / radius) * self.steer_ratio

        return max(self.min_angle, min(self.max_angle, angle))

    def get_steering(self, linear_velocity, angular_velocity, current_velocity, cur_angular, sample_time):
        angular_velocity = current_velocity * angular_velocity / linear_velocity if abs(linear_velocity) > 0. else 0.
        #angular_velocity = self.cte_pid.step(angular_velocity, sample_time)
        if abs(current_velocity) > 0.1:
            max_yaw_rate = abs(self.max_lat_accel / current_velocity)
            angular_velocity = max(-max_yaw_rate, min(max_yaw_rate, angular_velocity))

        return self.get_angle(max(current_velocity, self.min_speed) / angular_velocity) if abs(angular_velocity) > 0. else 0.0

    def steering_PID (self, angular_velocity, angular_current, dbw_enable):
        pass