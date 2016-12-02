import math

class DTLZ5():
    def calc_objectives(self, individual, objs):
        f = []
        g = 0.

        for x in individual.features[objs - 1:]:
            g = g + (x - .5) ** 2
        theta = [math.pi * individual.features[0] * .5]

        for x in individual.features[1:objs - 1]:
            theta.append((1 + 2 * g * x) * math.pi / (4 * (1 + g)))

        for i in xrange(objs):
            tmp = 1 + g

            for x in theta[:objs - 1 - i]:
                tmp = tmp * math.cos(x * math.pi * .5)

            if not i == 0:
                tmp = tmp * math.sin(theta[objs - i - 1] * math.pi / 2)

            f.append(tmp)

        return f

    def perfect_pareto_front(self):
        pass