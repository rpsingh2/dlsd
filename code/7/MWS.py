from DTLZ7 import *
import random
import math

decisions = [0]
energy = 0


def P(old, new, t):
    try:
        ans = math.exp((old - new) / t)
    except OverflowError:
        ans = 2
    return ans

def sa(problem=DTLZ7(), init_val=[1, 1]):
    t = 1
    t_max = 1000
    new_point = problem.generate_one()
    problem.evaluate(new_point)
    current_point = new_point
    best_point = new_point

    while t < t_max:

        if 0.5 < random.random():
            new_point = problem.local_search(new_point)

        if best_point.objectives[0] > new_point.objectives[0]:
            best_point = new_point

        if current_point.objectives[0] > new_point.objectives[0]:
            current_point = new_point

        new_point = problem.generate_one()
        problem.evaluate(new_point)

        t += 1

    return best_point.objectives[0]
    #print "Best decisions: " + str([str(dec['value']) for dec in best.point.decisions])
    #print "Best energy:    " + str(best.point.energy)

print sa()