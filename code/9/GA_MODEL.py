from util import *
import random

def populate(problem, size):
    population = []
    while(len(population) < size):
        population.append(problem.generate_one())
    return population

def crossover(mom, dad):
    # the first half of mom and second half of dad
    n = len(mom.decisions)
    return Point(mom.decisions[:n//2] + dad.decisions[n//2:])

def mutate(problem, point, mutation_rate=0.01):
    # and if the probability is less than mutation rate
    # change the decision(randomly set it between its max and min).
    for x, y in enumerate(point.decisions):
        if random.random() < mutation_rate: y = random_value(problem.decisions[x].low, problem.decisions[x].high)
    return point

def bdom(problem, one, two):
    """
    Return if one dominates two
    """
    # of bdom above.
    objs_one = problem.evaluate(one)
    objs_two = problem.evaluate(two)
    dominates = False

    for i in xrange(len(objs_one)):
        if 'Min' in problem.objectives[i].name:
            if objs_two[i] < objs_one[i]:
                return False
            elif objs_one[i] < objs_two[i]:
                dominates = True
        else:
            for i in xrange(len(objs_one)):
                if objs_two[i] > objs_one[i]:
                    return False
                elif objs_one[i] > objs_two[i]:
                    dominates = True
    if dominates:
        return True
    return False

def fitness(problem, population, point):
    # For this workshop define fitness of a point
    # as the number of points dominated by it.
    # For example point dominates 5 members of population,
    # then fitness of point is 5.
    dominates = 0
    for p in population:
        if (p != point) and (bdom(problem, point, p)):
            dominates += 1
    return dominates

def elitism(problem, population, retain_size):
    # of the points and return the top 'retain_size' points of the population
    d = dict()
    for p in population:
        d[p] = fitness(problem, population, p)
    return sorted(population, key=lambda x: d[x], reverse=True)[:retain_size]

import matplotlib.pyplot as plt
def plot_pareto(initial, final):
    initial_objs = [point.objectives for point in initial]
    final_objs = [point.objectives for point in final]
    initial_x = [i[0] for i in initial_objs]
    initial_y = [i[1] for i in initial_objs]
    final_x = [i[0] for i in final_objs]
    final_y = [i[1] for i in final_objs]
    plt.scatter(initial_x, initial_y, color='b', marker='+', label='initial')
    plt.scatter(final_x, final_y, color='r', marker='o', label='final')
    plt.title("Scatter Plot between initial and final population of GA")
    plt.ylabel("Total Surface Area(T)")
    plt.xlabel("Curved Surface Area(S)")
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.175), ncol=2)
    plt.show()

def ga(problem = DTLZ1(), pop_size = 200, gens = 10, mutation_rate = 0.5):
    population = populate(problem, pop_size)
    [problem.evaluate(point) for point in population]
    initial_population = [point.clone() for point in population]
    gen = 0
    while gen < gens:
        say(" " + str(gen))
        children = []
        for _ in range(pop_size):
            mom = random.choice(population)
            dad = random.choice(population)
            while (mom == dad):
                dad = random.choice(population)
            child = mutate(problem, crossover(mom, dad), mutation_rate)
            if problem.is_valid(child) and child not in population+children:
                children.append(child)
        population += children
        population = elitism(problem, population, pop_size)
        gen += 1
    print("")
    return initial_population, population


#initial, final = ga()
#plot_pareto(initial, final)