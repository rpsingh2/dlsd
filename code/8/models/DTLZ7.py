import math

class DTLZ7():
    def g(self, individual, objs):
        g = len(individual.features) - objs + 1
        for x in individual.features[objs - 1:]:
            g += (x - 0.5) ** 2 - math.cos(20 * math.pi * (x - 0.5))
        return g * 100.

    def calc_objectives(self, individual, objs):
        f = []

        g = 1 + 9 / (len(individual.features) - objs + 1) * sum(individual.features[objs - 1:])
        h = objs
        for i in range(objs - 1):
            f.append(individual.features[i])
            h = h - f[i] / (1 + g) * (1 + math.sin(3 * math.pi * f[i]))
        f.append((1 + g) * h)
        return f

    def perfect_pareto_front(self):
        pass