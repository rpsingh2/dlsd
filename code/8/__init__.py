from individual import Individual
from problems import Problem
import random
import functools
import math

def cdom(x, y):
    def expLoss(w, x1, y1, n):
        return -1 * (w * (x1 - y1) / n)

    def loss(x, y):
        losses = []
        n = min(len(x), len(y))
        for obj in range(n):
            x1, y1 = x[obj], y[obj]
            losses += [expLoss(-1, x1, y1, n)]
        return sum(losses) / n
    l1 = loss(x, y)
    l2 = loss(y, x)
    return l1 < l2


def bdom(x, y):
    for i in range(len(x)):
        if x[i] > y[i]:
            return False
    return True

class DTLZ(Problem):

    def __init__(self, zdt_definitions, num_decisions, num_objectives, domination = "bdom"):
        self.zdt_definitions = zdt_definitions
        self.num_decisions = num_decisions
        self.num_objectives = num_objectives
        self.max_objectives = [None for _ in range(num_objectives)]
        self.min_objectives = [None for _ in range(num_objectives)]
        self.domination_type = domination
        self.problem_type = None

    def __dominates(self, individual2, individual1):
        return bdom(individual1.objectives, individual2.objectives)

    def generateIndividual(self):
        individual = Individual()
        individual.features = []
        for i in range(self.num_decisions):
            individual.features.append(random.random())
        individual.dominates = functools.partial(self.__dominates, individual1=individual)
        self.calculate_objectives(individual)
        return individual

    def calculate_objectives(self, individual):
        individual.objectives = self.zdt_definitions.calc_objectives(individual, self.num_objectives)
        for i in range(self.num_objectives):
            if self.min_objectives[i] is None or individual.objectives[i] < self.min_objectives[i]:
                self.min_objectives[i] = individual.objectives[i]
            if self.max_objectives[i] is None or individual.objectives[i] > self.max_objectives[i]:
                self.max_objectives[i] = individual.objectives[i]
