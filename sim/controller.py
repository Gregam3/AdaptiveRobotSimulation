import random
import numpy as np

import assignment
import enum
from filterpy.gh import GHFilter

MOVE_MAX = 50

move_count = MOVE_MAX
rotate_count = 0
orient_count = 0

g=0.1
h=0.1


highest_read = -1.0
rotation_at_highest_read = -1
hit_light = False
ever_hit_light = False
cumulativeSensors = []
filter = None


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
    global cumulativeSensors
    if hit_light:
        return get_home()
    else:
        cumulativeSensors.append(sensors[0])

        return find_light(sensors, dt)


def move_towards_light(filtered_sensor):
    global move_count, hit_light, ever_hit_light

    if filtered_sensor[1][0] > 1:
        move_count = 0
        hit_light = True
        ever_hit_light = True

    return move(False)


def find_light(sensor_reading, dt):
    global filter

    filtered_sensor = update_filter(sensor_reading, dt)

    if move_count <= MOVE_MAX:
        return move_towards_light(filtered_sensor)
    else:
        if rotate_count <= 40:
            return search(filtered_sensor)
        elif not (rotation_at_highest_read == orient_count):
            return rotate_to_highest_read()
        else:
            reset(False)

            return [0, 0], None


def update_filter(sensorValue, dt):
    global filter

    if filter is None:
        filter = GHFilter(x=sensorValue, dx=0, dt=dt, g=g, h=h)
        return filter.update(sensorValue)
    else:
        return filter.update(sensorValue)


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


circle_count = 0
rotateBeforeCircle = 0


def get_home():
    global hit_light, move_count, circle_count, rotateBeforeCircle

    if move_count > 100:
        if circle_count > ((100 * 2) * np.pi) / 3:
            hit_light = False
            circle_count = 0
        elif rotateBeforeCircle <= 10:
            rotateBeforeCircle += 1
            return rotate()
        else:
            circle_count += 1

            if circle_count % 7 == 0:
                return rotate()
            else:
                return move(True)

    move_count += 1

    return move(True)
