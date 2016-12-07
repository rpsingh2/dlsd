from __future__ import print_function, division
from math import *
import random
import sys

# TODO 1: Enter your unity ID here
__author__ = "zithomas"


class O:
    """
    Basic Class which
        - Helps dynamic updates
        - Pretty Prints
    """

    def __init__(self, **kwargs):
        self.has().update(**kwargs)

    def has(self):
        return self.__dict__

    def update(self, **kwargs):
        self.has().update(kwargs)
        return self

    def __repr__(self):
        show = [':%s %s' % (k, self.has()[k])
                for k in sorted(self.has().keys())
                if k[0] is not "_"]
        txt = ' '.join(show)
        if len(txt) > 60:
            show = map(lambda x: '\t' + x + '\n', show)
        return '{' + ' '.join(show) + '}'


print("Unity ID: ", __author__)

# Few Utility functions
def say(*lst):
    """
    Print whithout going to new line
    """
    print(*lst, end="")
    sys.stdout.flush()


def random_value(low, high, decimals=2):
    """
    Generate a random number between low and high.
    decimals incidicate number of decimal places
    """
    return round(random.uniform(low, high), decimals)


def gt(a, b): return a > b


def lt(a, b): return a < b


def shuffle(lst):
    """
    Shuffle a list
    """
    random.shuffle(lst)
    return lst


class Decision(O):
    """
    Class indicating Decision of a problem
    """

    def __init__(self, name, low, high):
        """
        @param name: Name of the decision
        @param low: minimum value
        @param high: maximum value
        """
        O.__init__(self, name=name, low=low, high=high)


class Objective(O):
    """
    Class indicating Objective of a problem
    """

    def __init__(self, name, do_minimize=True):
        """
        @param name: Name of the objective
        @param do_minimize: Flag indicating if objective has to be minimized or maximized
        """
        O.__init__(self, name=name, do_minimize=do_minimize)


class Point(O):
    """
    Represents a member of the population
    """

    def __init__(self, decisions):
        O.__init__(self)
        self.decisions = decisions
        self.objectives = None

    def __hash__(self):
        return hash(tuple(self.decisions))

    def __eq__(self, other):
        return self.decisions == other.decisions

    def clone(self):
        new = Point(self.decisions)
        new.objectives = self.objectives
        return new

from hypervolume import *
def hv(population, num_objectives):
    referencePoint = [11 for _ in range(num_objectives)]
    hv = InnerHyperVolume(referencePoint)

    volume = hv.compute(individual.objectives for individual in population)
    return volume

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

    #x = x.objectives[:]
    #y = y.objectives[:]
    l1 = loss(x, y)
    return -l1

# Few Utility functions
def say(*lst):
    """
    Print whithout going to new line
    """
    print(*lst, end="")
    sys.stdout.flush()

class NSGAII_PROBLEM(O):
    def __init__(self, prob_name, num_dec, num_obj):
        O.__init__(self)
        self.decisions = [Decision("pop_size", 20, 100), Decision("generations", 10, 50), Decision("mutation rate", 0, 1)]
        self.objectives = [Objective("Max") for _ in xrange(1)]

        self.problem_name = prob_name
        self.problem_dec = num_dec
        self.problem_obj = num_obj

    def evaluate(self, point):
        from nsgaii import NSGAII
        from models import MODEL
        from models.DTLZ1 import DTLZ1
        from models.DTLZ3 import DTLZ3
        from models.DTLZ5 import DTLZ5
        from models.DTLZ7 import DTLZ7
        problem = ''
        if self.problem_name == 'dtlz1': problem = MODEL(self.problem_name, DTLZ1(), self.problem_dec, self.problem_obj)
        if self.problem_name == 'dtlz3': problem = MODEL(self.problem_name, DTLZ3(), self.problem_dec, self.problem_obj)
        if self.problem_name == 'dtlz5': problem = MODEL(self.problem_name, DTLZ5(), self.problem_dec, self.problem_obj)
        if self.problem_name == 'dtlz7': problem = MODEL(self.problem_name, DTLZ7(), self.problem_dec, self.problem_obj)
        nsga = NSGAII(problem, point.decisions[0], point.decisions[1], point.decisions[2])
        hypervolume, final_pop = nsga.run()
        #f = [hv(final, self.problem.num_objectives)]
        point.objectives = [hypervolume]
        return hypervolume

    def is_valid(self, point):
        if isinstance(point.decisions[0], float) or isinstance(point.decisions[1], float):
            return False
        return True

    def generate_one(self):
        while (True):
            point = Point([
                int(random.randint(self.decisions[0].low, self.decisions[0].high)),
                int(random.randint(self.decisions[1].low, self.decisions[1].high)),
                random_value(self.decisions[2].low, self.decisions[2].high)
            ])
            if self.is_valid(point):
                return point