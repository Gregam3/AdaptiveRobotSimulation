import random

import assignment
import enum
<<<<<<< HEAD
from stack import stack



moveCount = 100
moveMax = 10
rotateCount = 0

rotateToCorrectAngleCount = 0

highestReadForRotation = -1.0
rotationAtHighestRead = -1

hitLight = False

movesToLight = stack()


def constantController(sensors, state, dt):
    if(hitLight): return getHome(sensors)
    else: return findLight(sensors)

def findLight(sensors):
    global moveCount, rotateCount, rotateToCorrectAngleCount, highestReadForRotation, rotationAtHighestRead, hitLight, movesToLight

    if moveCount < 100:
        if(sensors[0] > 12):
            hitLight = True
        print("moving")
        moveCount += 1
        movesToLight.push([1, 1])
        return [1, 1], None
    else:
        if rotateCount < 40:
            print('searching', sensors[0], highestReadForRotation, rotateCount)
            if(sensors[0] > highestReadForRotation):
                highestReadForRotation = sensors[0]
                rotationAtHighestRead = rotateCount

            rotateCount += 1

            #Inverted move
            movesToLight.push([1, -1])
            return [1, -1], None
        elif not (rotationAtHighestRead == rotateToCorrectAngleCount):
            rotateToCorrectAngleCount += 1
            print('rotating', highestReadForRotation, rotateToCorrectAngleCount)
            print(rotateToCorrectAngleCount, highestReadForRotation)


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
    global movesToLight

    while(movesToLight.size() > 0):
        move = movesToLight.pop()
        return [move[0] * -1, move[1] * - 1], None

    return [0,0], None
=======


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

>>>>>>> f401e645680f4e30c7ebe2c44be72a394404ebd8


w = assignment.World()
poses, sensations, actions, states = w.simulate(constantController)
print("Fitness on task 1: %f" % w.task1fitness(poses))
print("Fitness on task 2: %f" % w.task2fitness(poses))
ani = w.animate(poses, sensations)
