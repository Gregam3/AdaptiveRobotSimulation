import random
import numpy as np

import assignment
import enum
from filterpy.gh import GHFilter

MOVE_MAX = 50

move_count = MOVE_MAX
rotate_count = 0
orient_count = 0

highest_read = -1.0
rotation_at_highest_read = -1
hit_light = False

circle_count = 0
rotate_before_circle = 0


def reset(full_reset):
    global move_count, rotate_count, orient_count, highest_read, \
        rotation_at_highest_read, hit_light, ever_hit_light, circle_count
    if full_reset:
        move_count = MOVE_MAX
        ever_hit_light = False
    else:
        move_count = 0

    rotate_count = 0
    orient_count = 0
    highest_read = -1.0
    rotation_at_highest_read = -1
    circle_count = 0
    hit_light = False


def constant_controller(sensors, state, dt):
    if hit_light: return get_home()
    else: return find_light(sensors, dt)


def move_towards_light(sensor_value):
    global move_count, hit_light, ever_hit_light

    if sensor_value > 1:
        move_count = 0
        hit_light = True
        ever_hit_light = True

    return move(False)


def find_light(sensor_reading, dt):
    if move_count <= MOVE_MAX:
        return move_towards_light(sensor_reading)
    else:
        if rotate_count <= 40: return search(sensor_reading)
        elif not (rotation_at_highest_read == orient_count): return rotate_to_highest_read()
        else:
            reset(False)
            return find_light(sensor_reading, dt)


def search(filteredSensor):
    global highest_read, rotation_at_highest_read, rotate_count

    if filteredSensor > highest_read:
        highest_read = filteredSensor
        rotation_at_highest_read = rotate_count

    rotate_count += 1

    return rotate()


def rotate_to_highest_read():
    global orient_count
    orient_count += 1

    return rotate()


def move(backwards):
    global move_count, ever_hit_light

    move_count += 1

    if not backwards:
        return [10, 10], None
    else:
        return [-10, -10], None


def rotate():
    return [1, -1], None


def get_home():
    global hit_light, move_count, circle_count, rotate_before_circle

    if move_count > 100:
        if circle_count > ((100 * 2) * np.pi) / 3:
            hit_light = False
            circle_count = 0
        elif rotate_before_circle <= 10:
            rotate_before_circle += 1
            return rotate()
        else:
            circle_count += 1

            if circle_count % 7 == 0:
                return rotate()
            else:
                return move(True)

    move_count += 1

    return move(True)
