import random
import numpy as np

import assignment
import enum
from stack import stack
from filterpy.gh import GHFilter

moveCount = 100
moveMax = 10
rotateCount = 0
moveCountUntilLightHit = 0

rotateToCorrectAngleCount = 0

highestReadForRotation = -1.0
rotationAtHighestRead = -1

hitLight = False
everHitLight = False

cumulativeSensors = []

filter = None

def reset(moveCountToInitial):
    global moveCount, rotateCount, rotateToCorrectAngleCount, highestReadForRotation, rotationAtHighestRead, hitLight, movesToLight, everHitLight, moveCountUntilLightHit, circleCount
    if (moveCountToInitial):
        moveCount = 100
        everHitLight = False
    else:
        moveCount = 0
    rotateCount = 0

    rotateToCorrectAngleCount = 0

    highestReadForRotation = -1.0
    rotationAtHighestRead = -1

    moveCountUntilLightHit = 0
    circleCount = 0


    hitLight = False

    movesToLight = stack()


def constantController(sensors, state, dt):
    global cumulativeSensors
    if hitLight:
        return getHome()
    else:
        cumulativeSensors.append(sensors[0])

        return findLight(dt, sensors)



def moveTowardsLight(filteredSensor):
    global moveCount, hitLight

    # print('Filter value', filteredSensor[1][0])

    if filteredSensor[1][0] > 1:
        # print('Hit Light', filteredSensor[1][0])
        moveCount = 0
        hitLight = True
        everHitLight = True

    return move(False)

def findLight(dt, sensorValue):
    global filter

    filteredSensor = None

    if(filter == None):
        print('filter init')
        filter = GHFilter(x=sensorValue, dx=0, dt=dt, g=0.1, h=0.1)

        filteredSensor = filter.update(sensorValue)
    else:
        filteredSensor = filter.update(sensorValue)

    # print('moving' ,filteredSensor)

    if moveCount <= 50:
        return moveTowardsLight(filteredSensor)
    else:
        if rotateCount <= 40:
            return search(filteredSensor)
        elif not (rotationAtHighestRead == rotateToCorrectAngleCount):
            return rotateToHighestRead()
        else:
            reset(False)

            return [0, 0], None


def search(filteredSensor):
    global highestReadForRotation, rotationAtHighestRead, rotateCount

    # print('Searching')

    if filteredSensor > highestReadForRotation:
        highestReadForRotation = filteredSensor
        rotationAtHighestRead = rotateCount

    rotateCount += 1

    return rotate()


def rotateToHighestRead():
    global rotateToCorrectAngleCount
    rotateToCorrectAngleCount += 1

    # print('Orienting')

    return rotate()


def move(backwards):
    global moveCount, everHitLight, moveCountUntilLightHit

    if not (everHitLight): moveCountUntilLightHit += 1
    moveCount += 1

    if not (backwards):
        return [10, 10], None
    else:
        return [-10, -10], None


def rotate():
    return [1, -1], None


circleCount = 0
rotateBeforeCircle = 0

def getHome():
    global hitLight, moveCount, circleCount, rotateBeforeCircle

    if (moveCount > moveCountUntilLightHit * 1.55):
        if (circleCount > ((moveCountUntilLightHit * 2) * np.pi) / 10):
            hitLight = False
        elif(rotateBeforeCircle <= 10):
            rotateBeforeCircle += 1
            return rotate()
        else:
            circleCount += 1

            if(circleCount % 8 == 0):
                return rotate()
            else:
                return move(True)


    moveCount += 1

    return move(True)


def runSimulations(count):
    global highestSuccessfulTask2Count, highestG, highestH

    task1Cumulative = 0
    task2Cumulative = 0

    successfulTask1Count = 0.0
    successfulTask2Count = 0.0

    for i in range(1, count + 1):
        w = assignment.World()
        poses, sensations, actions, states = w.simulate(constantController)

        reset(True)

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
        print("g=%f" % g)
        print("h=%f" % h)
        print("=" * 33)

        # if not (t2f == -np.inf):
        # ani = w.animate(poses, sensations)

    if successfulTask1Count > 0:
        print("Task 1 average fitness: %f" % (task1Cumulative / successfulTask1Count))
    else:
        print("Task 1 succeeded 0 times")

    print("Task 1 Success rate: %f%%" % (
                (successfulTask1Count / count * 1.0) * 100) if successfulTask1Count > 0 else '0%')

    if successfulTask2Count > 0:
        print("Task 2 average fitness: %f" % (task2Cumulative / successfulTask2Count))

        if(successfulTask2Count > highestSuccessfulTask2Count):
                highestSuccessfulTask2Count = successfulTask2Count
                highestG = g
                highestH = h
    else:
        print("Task 2 succeeded 0 times")

    print(
        "Task 2 Success rate: %f%%" % ((successfulTask2Count / count * 1.0) * 100) if successfulTask2Count > 0 else '')


g = 0
h = 0
highestG = 0
highestH = 0
highestSuccessfulTask2Count = 0

# def run():
#     global g, h
#     for i in range(0, 100):
#         g = random.uniform(0,1)
#         h = random.uniform(0,1)
#
#         runSimulations(250)
#
#         print(highestSuccessfulTask2Count, highestG, highestH)
#
# run()

runSimulations(500)
