from DTLZ7 import *
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


def rand_one(lst):
  return random.choice(lst)

def three_others(one, pop):
    """
    Return three other points from population
    :param one: Point not to consider
    :param pop: Population to look in
    :return: two, three, four
    """

    def one_other():
        while True:
            x = rand_one(pop)
            if not str(x) in seen:
                seen.append(str(x))
                return x

    seen = [str(one)]
    two = one_other()
    three = one_other()
    four = one_other()
    return two, three, four

def mutate(problem, point, population, crossover_rate=0.3, mutation_factor = 0.75):
    # and if the probability is less than mutation rate
    # change the decision(randomly set it between its max and min).
    mutated_point = point.clone()

    num_decisions = len(problem.decisions)
    while(True):
        two, three, four = three_others(mutated_point, population)
        random_index  = rand_one(range(num_decisions))
        mutated_decisions = mutated_point.decisions[:]
        for i in range(num_decisions):
          if (random.random() < crossover_rate) or (i == random_index):
            mutated_decisions[i] = (two.decisions[i] + mutation_factor *(three.decisions[i] - four.decisions[i]))

        mutated_point.decisions = mutated_decisions
        if problem.is_valid(mutated_point):
            break

    return mutated_point


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


def select(problem, population):
    clones = []
    for one in population:
        problem.evaluate(one)
        clones.append( one )

    return clones


def evolve(problem, selected, population):
    for point in population:
        problem.evaluate(point)
        mutant = mutate(problem, point, population)
        problem.evaluate(mutant)
        if bdom(problem, mutant, point):
            selected.remove(point)
            selected.append(mutant)
    return selected

def de(problem = DTLZ7(), init_val = [0, 0], pop_size = 100, gens = 10):
    population = populate(problem, pop_size)
    [problem.evaluate(point) for point in population]
    initial_population = [point.clone() for point in population]
    gen = 0
    while gen < gens:
        selected = select(problem, population)
        population = evolve(problem, selected, population)
        gen += 1
    #print("")
    obs = [ind.objectives[0] for ind in population]

    import matplotlib.pyplot as plt
    plt.scatter(problem.plotter_x, problem.plotter_y)
    return min(obs)
    #return initial_population, population

print de()