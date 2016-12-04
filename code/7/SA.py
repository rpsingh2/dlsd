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
    current_point = Point.clone(new_point)
    best_point = Point.clone(new_point)

    while t < t_max:
        new_point = problem.generate_one()
        problem.evaluate(new_point)

        if best_point.objectives[0] > new_point.objectives[0]:
            best_point = Point.clone(new_point)

        if current_point.objectives[0] > new_point.objectives[0]:
            current_point = Point.clone(new_point)

        if P(current_point.objectives[0], new_point.objectives[0], float(t) / t_max) < random.random():
            current_point = Point.clone(new_point)
        t += 1

    import matplotlib.pyplot as plt
    plt.scatter(problem.plotter_x, problem.plotter_y)
    return best_point.objectives[0]

print sa()