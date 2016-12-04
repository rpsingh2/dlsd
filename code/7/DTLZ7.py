from __future__ import print_function, division
from math import *
import random
import sys


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
        return self.decisions == other.decisions[:]


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


class DTLZ7(O):
    def __init__(self, num_decisions = 2, num_objectives = 1):
        O.__init__(self)
        # using the auxilary classes provided above.
        self.decisions = [Decision("", 0, 1) for _ in xrange(num_decisions)]
        self.objectives = [Objective("Min") for _ in xrange(num_objectives)]

        self.num_decisions = num_decisions
        self.num_objectives = num_objectives

        self.best_val_array = self.best_vals()

        self.plotter_x = []
        self.plotter_y = []

    def best_vals(self):
        import csv
        with open('best_vals.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            bv = []
            for row in spamreader:
                bv.append(row)
        return bv

    def igd(self, coord):
        import sys, math
        best_distance = sys.maxint
        for x in self.best_val_array:
            dist = math.sqrt( (coord[0] - float(x[0]))**2 + (coord[1] - float(x[1]))**2 )
            if best_distance > dist: best_distance = dist
        return best_distance


    def g(self, point):
        return (1 + (9 / self.num_decisions * sum(point.decisions)))

    def h(self, point):
        import math
        sum = 0
        count = 0
        while count <= self.num_objectives - 1:
            sum += (point.decisions[count]/(1+self.g(point))) * (1 + math.sin(3 * math.pi * point.decisions[count]))
            count += 1
        return self.num_objectives - sum

    def evaluate(self, point):
        import math
        m = self.num_objectives
        n = self.num_decisions
        multiplier = 1 / floor(n / m)

        g = self.g(point)
        h = self.h(point)

        f = []
        f = point.decisions[:-1]
        f.append(1 + g * h)
        self.plotter_x.append(f[0])
        self.plotter_y.append(f[1])
        point.objectives = [self.igd(f)]
        return point.objectives

    def is_valid(self, point):
        if len([x for x in point.decisions if x < 0]) > 0: return False
        return True

    def local_search(self, point):
        num_dec = self.num_decisions

        dec_num = random.randint(0, num_dec - 1)

        distribution = [x/10 for x in xrange(10)]
        best_pt = Point.clone(point)
        for dis in distribution:
            new_pt = Point.clone(point)
            new_pt.decisions[dec_num] = dis
            self.evaluate(new_pt)
            if point.objectives[0] > new_pt.objectives[0]:
                best_pt = new_pt

        return best_pt


    def generate_one(self):
        while (True):
            point = Point([random_value(d.low, d.high) for d in self.decisions])
            if self.is_valid(point):
                return point
            else:
                print("try again")