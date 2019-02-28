import random

import assignment
import enum


class State(enum.Enum):
    rotating = 1
    forward = 2


moveCount = 0
moveMax = 10
rotateCount = 0


def constantController(sensors, state, dt):
    global moveCount, rotateCount, moveMax

    if moveCount < moveMax:
        print("moving")
        moveCount += 1
        return [1, 1], None
    else:

        if rotateCount > 50:
            moveCount = 0
            rotateCount = 0
            moveMax += 10

        rotateCount += 1
        return [1, -1], None



w = assignment.World()
poses, sensations, actions, states = w.simulate(constantController)
print("Fitness on task 1: %f" % w.task1fitness(poses))
print("Fitness on task 2: %f" % w.task2fitness(poses))
ani = w.animate(poses, sensations)
