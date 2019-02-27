from sim import assignment


def constantController(sensors, state, dt):

    return [1, 3], None


w = assignment.World()
poses, sensations, actions, states = w.simulate(constantController)
print("Fitness on task 1: %f" % w.task1fitness(poses))
print("Fitness on task 2: %f" % w.task2fitness(poses))
ani = w.animate(poses, sensations)
