from controller import constant_controller
import assignment
from controller import reset
import numpy as np

def run_simulations(count):
    global highest_successful_task2_count, highestG, highestH

    task1_cumulative = 0
    task2_cumulative = 0

    successful_task1_count = 0.0
    successful_task2_count = 0.0

    for i in range(1, count + 1):
        w = assignment.World()
        poses, sensations, actions, states = w.simulate(constant_controller)

        reset(True)

        t1f = w.task1fitness(poses)
        t2f = w.task2fitness(poses)

        if not t1f == -np.inf:
            successful_task1_count += 1
            task1_cumulative += t1f

        if not t2f == -np.inf:
            successful_task2_count += 1
            task2_cumulative += t2f

        print("Simulation - %d |" % i)
        print("-----------------")
        print("Fitness on task 1: %f" % w.task1fitness(poses))
        print("Fitness on task 2: %f" % w.task2fitness(poses))
        # print("g=%f" % g)
        # print("h=%f" % h)
        print("=" * 33)

        # if not (t2f == -np.inf):
        # ani = w.animate(poses, sensations)

    if successful_task1_count > 0:
        print("Task 1 average fitness: %f" % (task1_cumulative / successful_task1_count))
    else:
        print("Task 1 succeeded 0 times")

    print("Task 1 Success rate: %f%%" % (
            (successful_task1_count / count * 1.0) * 100) if successful_task1_count > 0 else '0%')

    if successful_task2_count > 0:
        print("Task 2 average fitness: %f" % (task2_cumulative / successful_task2_count))

        # if successful_task2_count > highest_successful_task2_count:
        #     highest_successful_task2_count = successful_task2_count
        #     highestG = g
        #     highestH = h
    else:
        print("Task 2 succeeded 0 times")

    print(
        "Task 2 Success rate: %f%%" % ((successful_task2_count / count * 1.0) * 100) if successful_task2_count > 0 else '')


# g = 0
# h = 0
# highestG = 0
# highestH = 0
# highest_successful_task2_count = 0

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

run_simulations(500)
