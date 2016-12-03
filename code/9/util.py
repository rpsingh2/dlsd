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


class Problem(O):
    """
    Class representing the cone problem.
    """

    def __init__(self):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("radius", 0, 10), Decision("height", 0, 20)]
        self.objectives = [Objective("Min S"), Objective("Min T")]

    @staticmethod
    def evaluate(point):
        [r, h] = point.decisions
        l = (r ** 2 + h ** 2) ** (1 / 2)
        S = pi * r * l
        T = S + pi * r ** 2
        point.objectives = [S, T]
        # TODO 3: Evaluate the objectives S and T for the point.
        return point.objectives

    @staticmethod
    def is_valid(point):
        [r, h] = point.decisions
        r2 = r ** 2
        V = (pi / 3) * r2 * h
        return V > 200
        # TODO 4: Check if the point has valid decisions

    def generate_one(self):
        # TODO 5: Generate a valid instance of Point.
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if Problem.is_valid(point):
                return point

class DTLZ1(O):
    def __init__(self, num_decisions = 2, num_objectives = 2):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("", 0, 1) for _ in xrange(num_decisions)]
        self.objectives = [Objective("Min") for _ in xrange(num_objectives)]

        self.num_decisions = num_decisions
        self.num_objectives = num_objectives

    def evaluate(self, point):
        import math
        m = self.num_objectives
        n = self.num_decisions
        k = n - m + 1
        g = 0
        for i in range(n - k, n):
            g += ((point.decisions[i] - 0.5) ** 2 - cos(20.0 * math.pi * (point.decisions[i] - 0.5)))
        g = 100 * (k + g)
        f = []
        for i in range(0, m): f.append((1.0 + g) * 0.5)
        for i in xrange(m):
            for j in range(0, m - (i + 1)): f[i] *= point.decisions[j]
            if not (i == 0):
                aux = m - (i + 1)
                f[i] *= 1 - point.decisions[aux]
        point.objectives = f
        return point.objectives

    @staticmethod
    def is_valid(point):
        return True

    def generate_one(self):
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
                return point

class DTLZ1(O):
    def __init__(self, num_decisions = 2, num_objectives = 2):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("", 0, 1) for _ in xrange(num_decisions)]
        self.objectives = [Objective("Min") for _ in xrange(num_objectives)]

        self.num_decisions = num_decisions
        self.num_objectives = num_objectives

    def evaluate(self, point):
        import math
        m = self.num_objectives
        n = self.num_decisions
        k = n - m + 1
        g = 0
        for i in range(n - k, n):
            g += ((point.decisions[i] - 0.5) ** 2 - cos(20.0 * math.pi * (point.decisions[i] - 0.5)))
        g = 100 * (k + g)
        f = []
        for i in range(0, m): f.append((1.0 + g) * 0.5)
        for i in xrange(m):
            for j in range(0, m - (i + 1)): f[i] *= point.decisions[j]
            if not (i == 0):
                aux = m - (i + 1)
                f[i] *= 1 - point.decisions[aux]
        point.objectives = f
        return point.objectives

    @staticmethod
    def is_valid(point):
        return True

    def generate_one(self):
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
                return point

class DTLZ3(O):
    def __init__(self, num_decisions = 2, num_objectives = 2):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("", 0, 1) for _ in xrange(num_decisions)]
        self.objectives = [Objective("Min") for _ in xrange(num_objectives)]

        self.num_decisions = num_decisions
        self.num_objectives = num_objectives

    def evaluate(self, point):
        import math
        m = self.num_objectives
        n = self.num_decisions
        k = n - m + 1
        g = 0
        for i in range(n - k, n):
            g += ((point.decisions[i] - 0.5) ** 2 - cos(20.0 * math.pi * (point.decisions[i] - 0.5)))
        g = 100 * (k + g)
        f = [1 + g] * m
        for i in range(0, m):
            for j in range(0, m - (i + 1)):
                f[i] *= cos(point.decisions[j] * math.pi / 2)
            if i != 0:
                f[i] *= sin(point.decisions[m - (i + 1)] * math.pi / 2)

        point.objectives = f
        return point.objectives

    @staticmethod
    def is_valid(point):
        return True

    def generate_one(self):
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
                return point

class DTLZ5(O):
    def __init__(self, num_decisions = 2, num_objectives = 2):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("", 0, 1) for _ in xrange(num_decisions)]
        self.objectives = [Objective("Min") for _ in xrange(num_objectives)]

        self.num_decisions = num_decisions
        self.num_objectives = num_objectives

    def evaluate(self, point):
        import math
        m = self.num_objectives
        n = self.num_decisions
        k = n - m + 1
        # Compute g
        g = 0
        for i in range(n - k, n):
            g += point.decisions[i] ** 0.1
        # Compute theta
        theta = [point.decisions[0] * math.pi / 2]
        t = math.pi / (4 * (1 + g))
        for i in range(1, m - 1):
            theta.append(t * (1 + 2 * g * point.decisions[i]))
        # Compute f
        f = [1 + g] * m
        for i in range(0, m):
            for j in range(0, m - (i + 1)):
                f[i] *= cos(theta[j])
            if i != 0:
                f[i] *= sin(theta[m - (i + 1)])

        point.objectives = f
        return point.objectives

    @staticmethod
    def is_valid(point):
        return True

    def generate_one(self):
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
                return point

class DTLZ7(O):
    def __init__(self, num_decisions = 2, num_objectives = 2):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("", 0, 1) for _ in xrange(num_decisions)]
        self.objectives = [Objective("Min") for _ in xrange(num_objectives)]

        self.num_decisions = num_decisions
        self.num_objectives = num_objectives

    def evaluate(self, point):
        import math
        m = self.num_objectives
        n = self.num_decisions
        multiplier = 1 / floor(n / m)
        f = []
        for j in range(m):
            start = int(max(floor(j * n / m), 0))
            end = int(min(floor((j + 1) * n / m), n - 1))
            f_j = 0
            for i in range(start, end):
                f_j += point.decisions[i]
            f_j *= multiplier
            f.append(f_j)

        point.objectives = f
        return point.objectives

    def is_valid(self, point):
        f = self.evaluate(point)
        m = len(f)
        status = True
        offset = 0
        for i in range(len(f) - 1):
            g_i = f[-1] + 4 * f[i] - 1
            if g_i < 0:
                status = False
                offset += abs(g_i)
        min_val = sys.maxint
        for i in range(m - 1):
            for j in range(i + 1, m - 1):
                if i == j: continue
                sum_val = f[i] + f[j]
                if sum_val < min_val: min_val = sum_val
        g_m = 2 * f[-1] + min_val - 1
        if g_m < 0:
            status = False
            offset += abs(g_m)
        return status, offset

    def generate_one(self):
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
                return point

from hypervolume import *
def hv(population, num_objectives):
    referencePoint = [11 for _ in range(num_objectives)]
    hv = InnerHyperVolume(referencePoint)

    volume = hv.compute(individual.objectives for individual in population)
    return volume

class GA_PROBLEM(O):

    def __init__(self, problem):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("pop_size", 10, 100), Decision("generations", 10, 100), Decision("mutation rate", 0, 1)]
        self.objectives = [Objective("Max") for _ in xrange(1)]

        self.problem = problem

    def evaluate(self, point):
        from GA_MODEL import ga
        initial, final = ga(self.problem, point.decisions[0], point.decisions[1], point.decisions[2])
        f = [hv(final, self.problem.num_objectives)]
        point.objectives = f
        return point.objectives

    def is_valid(self, point):
        return True

    def generate_one(self):
        while (True):
            point = Point([
                int(random_value(self.decisions[0].low, self.decisions[0].high, 0)),
                int(random_value(self.decisions[1].low, self.decisions[1].high, 0)),
                random_value(self.decisions[2].low, self.decisions[2].high)
            ])
            if self.is_valid(point):
                return point