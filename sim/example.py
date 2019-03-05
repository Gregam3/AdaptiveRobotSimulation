import random

import assignment
import enum
import numpy as np

moveCount = 0
moveMax = 10
rotateCount = 0


def constantController(sensors, state, dt):
    global moveCount, rotateCount, moveMax

    if moveCount < moveMax:
        moveCount += 1
        return [1, 1], None
    else:

        if rotateCount > 50:
            moveCount = 0
            rotateCount = 0
            moveMax += 10

        rotateCount += 1
        return [1, -1], None



def runSimulations(count):
    global highestSuccessfulTask2Count, highestG, highestH

    task1Cumulative = 0
    task2Cumulative = 0

    successfulTask1Count = 0.0
    successfulTask2Count = 0.0

    for i in range(1, count + 1):
        w = assignment.World()
        poses, sensations, actions, states = w.simulate(constantController)

        t1f = w.task1fitness(poses)
        t2f = w.task2fitness(poses)

        if not t1f == -np.inf:
            successfulTask1Count += 1
            task1Cumulative += t1f

        if not t2f == -np.inf:
            successfulTask2Count += 1
            task2Cumulative += t2f

        print("Simulation - %d |" % i)
        print("-----------------")
        print("Fitness on task 1: %f" % w.task1fitness(poses))
        print("Fitness on task 2: %f" % w.task2fitness(poses))
        print("=" * 33)

        if successfulTask1Count > 0:
            print("Task 1 average fitness: %f" % (task1Cumulative / successfulTask1Count))
        else:
            print("Task 1 succeeded 0 times")

        print("Task 1 Success rate: %f%%" % (
                (successfulTask1Count / count * 1.0) * 100) if successfulTask1Count > 0 else '0%')

        if successfulTask2Count > 0:
                print("Task 2 average fitness: %f" % (task2Cumulative / successfulTask2Count))
        else:
            print("Task 2 succeeded 0 times")

        print("Task 2 Success rate: %f%%" % ((successfulTask2Count / count * 1.0) * 100) if successfulTask2Count > 0 else '')

runSimulations(100)
