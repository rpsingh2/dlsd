from __future__ import print_function, division
import sys; sys.dont_write_bytecode = True

import math, random


class DTLZ1:
    name = "DTLZ1"
    def __init__(self, num_objectives, num_decisions):
        self.name = "DTLZ1"
        self.num_decisions = num_decisions
        self.num_objectives = num_objectives
        self.dec_high = [1 for _ in range(self.num_decisions)]
        self.dec_low = [0 for _ in range(self.num_decisions)]
        self.dec = []
        self.cec_2 = []

    def function_value(self, dec, decs, objs):
        f = function_value(dec, decs, objs)
        return f

    def random_decs(self):
        while True:
            dec = list()
            for low, high in zip(self.dec_low, self.dec_high):
                dec.append(random.uniform(low, high))
            if self.ok(dec):
                break
        return dec

    def ok(self, dec):
        for i in range(0, self.num_decisions):
            if dec[i] < self.dec_low[i] or dec[i] > self.dec_high[i]:
                return False
        return True


def g(dec, objs, decs):
    g = decs - objs + 1
    for x in dec[objs - 1:]:
        g += (x - 0.5) ** 2 - math.cos(20 * math.pi * (x - 0.5))
    return g * 100.


def function_value(dec, decs, objs):
    f = []
    for i in range(objs):
        val = (1 + g(dec, objs, decs)) * 0.5
        for x in dec[:objs - (i + 1)]:
            val *= x
        if not i == 0:
            val = val * (1 - dec[objs - i])
        f.append(val)
    return f