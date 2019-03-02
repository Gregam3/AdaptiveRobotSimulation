import random
import numpy as np

import assignment
import enum
from stack import stack


moveCount = 100
moveMax = 10
rotateCount = 0

rotateToCorrectAngleCount = 0

highestReadForRotation = -1.0
rotationAtHighestRead = -1

hitLight = False

movesToLight = stack()



def reset():
    global moveCount, moveMax, rotateCount, rotateToCorrectAngleCount, highestReadForRotation, rotationAtHighestRead, hitLight, movesToLight
    moveCount = 100
    moveMax = 10
    rotateCount = 0

    rotateToCorrectAngleCount = 0

    highestReadForRotation = -1.0
    rotationAtHighestRead = -1

    hitLight = False

    spiral = 0.1

    movesToLight = stack()

def constantController(sensors, state, dt):
    if(hitLight): return getHome(sensors)
    else: return findLight(sensors)

def findLight(sensors):
    global moveCount, rotateCount, rotateToCorrectAngleCount, highestReadForRotation, rotationAtHighestRead, hitLight, movesToLight

    if moveCount < 50:
        if(sensors[0] > 1):
            hitLight = True
        # print("moving")
        moveCount += 1
        movesToLight.push([-1, -1])
        return [1, 1], None
    else:
        if rotateCount < 40:
            # print('searching', sensors[0], highestReadForRotation, rotateCount)
            if(sensors[0] > highestReadForRotation):
                highestReadForRotation = sensors[0]
                rotationAtHighestRead = rotateCount

            rotateCount += 1

            #Inverted move
            # movesToLight.push([1, -1])
            return [1, -1], None
        elif not (rotationAtHighestRead == rotateToCorrectAngleCount):
            rotateToCorrectAngleCount += 1
            # print('rotating', highestReadForRotation, rotateToCorrectAngleCount)
            # print(rotateToCorrectAngleCount, highestReadForRotation)


            return [1, -1], None
        else:
            highestReadForRotation = -1
            rotationAtHighestRead = -1
            moveCount = 0
            rotateCount = 0
            rotateToCorrectAngleCount = 0
            movesToLight.push([0, 0])
            return [0, 0], None



def getHome(sensors):

    return [-10, -10], None

def runSimulations(count):
    task1Cumulative = 0
    task2Cumulative = 0

    successfulTask1Count = 0.0
    successfulTask2Count = 0.0

    for i in range(1, count + 1):
        w = assignment.World()
        poses, sensations, actions, states = w.simulate(constantController)

        reset()

        t1f = w.task1fitness(poses)
        t2f = w.task2fitness(poses)

        if not t1f == -np.inf:
            successfulTask1Count += 1
            task1Cumulative += t1f

        if not t2f == -np.inf:
            successfulTask2Count += 1
            task2Cumulative += t2f

        # print("Simulation - %d |" % i)
        # print("-----------------")
        # print("Fitness on task 1: %f" % w.task1fitness(poses))
        # print("Fitness on task 2: %f" % w.task2fitness(poses))
        # print("=" * 33)

        if not (t2f - t1f < -80.0):
            # print("Simulation - %d |" % i)
            print("-----------------")
            print("Fitness on task 1: %f" % w.task1fitness(poses))
            print("Fitness on task 2: %f" % w.task2fitness(poses))
            print("=" * 33)
            ani = w.animate(poses, sensations)

    if successfulTask1Count > 0: print("Task 1 average fitness: %f" % (task1Cumulative / successfulTask1Count))
    else: print("Task 1 succeeded 0 times")

    print("Task 1 Success rate: %f%%" % ((successfulTask1Count / count * 1.0) * 100) if successfulTask1Count > 0 else '0%')

    if successfulTask2Count > 0: print("Task 2 average fitness: %f" % (task2Cumulative / successfulTask2Count))
    else: print("Task 2 succeeded 0 times")

    print("Task 2 Success rate: %f%%" % ((successfulTask2Count/ count * 1.0) * 100) if successfulTask2Count > 0 else '')

runSimulations(100)
