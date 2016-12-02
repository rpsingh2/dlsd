import math

class DTLZ3():
    def g(self, individual, objs):
        g = len(individual.features) - objs + 1
        for x in individual.features[objs - 1:]:
            g += (x - 0.5) ** 2 - math.cos(20 * math.pi * (x - 0.5))
        return g * 100.

    def calc_objectives(self, individual, objs):
        f = []
        for i in range(objs):
            val = (1 + self.g(individual, objs))
            for x in individual.features[:objs - (i + 1)]:
                val *= math.cos(x * math.pi * 0.5)
            if i != 0:
                val *= val * (math.sin(individual.features[objs - i] * math.pi * 0.5))
            f.append(val)
        return f

    def perfect_pareto_front(self):
        pass