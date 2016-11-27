from __future__ import print_function
import sys
import operator
import numpy as np


from fastNDOM import fast_nondominated_sort as fastNdom
from a12 import a12
from DTLZ1 import *

def say(*lst):
    """
    Print without going to new line
    :param lst:
    """
    print(*lst, end="")
    sys.stdout.flush()


class GA:
    def __init__(self, model, dominator='bdom', num_candidates=100, num_generations=1000, mutation_prob=0.05):
        self.num_objectives = model.num_objectives
        self.num_decisions = model.num_decisions
        self.num_candidates = num_candidates
        self.num_generations = num_generations
        self.mutation_prob = mutation_prob
        self.lives = 5
        self.frontier = []
        self.frontier_new = []
        self.base_frontier = []
        self.dominator = self.bdom if dominator == 'bdom' else self.cdom;

    def cdom(x, y, abouts):
        def w(better):
            def less(x, y): return x < y
            return -1 if better == less else 1

        def expLoss(w, x1, y1, n):
            return -1 * math.e ** (w * (x1 - y1) / n)

        def loss(x, y):
            losses = []
            n = min(len(x), len(y))
            for obj in range(x):
                x1, y1 = x[obj], y[obj]
                losses += [expLoss(w(obj.want), x1, y1, n)]
            return sum(losses) / n

        x = model.function_value(x, model.num_decisions, model.num_objectives)
        y = model.function_value(y, model.num_decisions, model.num_objectives)
        l1 = loss(x, y)
        l2 = loss(y, x)
        return l1 < l2

    def bdom(self, x, y):
        """
        Type I comparison
        Returns whether candidate x dominates candidate y (Binary domination)
        """
        x_obj_vec = model.function_value(x, model.num_decisions, model.num_objectives)
        y_obj_vec = model.function_value(y, model.num_decisions, model.num_objectives)

        for i in range(model.num_objectives):
            if x_obj_vec[i] > y_obj_vec[i]:
                return False
        return True

    def function_agg(self, x):
        """
        Returns the aggregate function value
        """
        x_obj_vec = model.function_value(x, model.num_decisions, model.num_objectives)
        return np.sum(x_obj_vec)

    def min_max(self, box):
        """
        Returns the maximum and minimum objective function vectors to calculate hypervolume
        """
        max_vector = [np.max([model.function_value(x, model.num_decisions, model.num_objectives)[i] for x in box]) for i
                      in range(model.num_objectives)]
        min_vector = [np.min([model.function_value(x, model.num_decisions, model.num_objectives)[i] for x in box]) for i
                      in range(model.num_objectives)]

        return max_vector, min_vector

    def select(self, box):
        """
        Selection Operation
        Return the candidate pool for new frontier 80% from child and 20% from random parents
        """
        fr = []
        d = dict()

        for i in range(len(box)):
            d[i] = self.function_agg(box[i])
        sorted_d = sorted(d.items(), key=operator.itemgetter(1))

        for j in range(int(self.num_candidates * .8)):
            fr.append(box[sorted_d[j][0]])

        for k in range(int(self.num_candidates * .2)):
            fr.append(self.frontier[k])

        return fr

    def crossover(self, parent_1, parent_2, child_1, child_2):
        """
        Crossover operation
        Picks a random decision, take all dad's decisions up to that point, take alll mum's decisions after that point
        """
        while True:
            rand_int = random.randint(0, model.num_decisions)
            child_1 = list(np.array(parent_1)[:rand_int]) + list(np.array(parent_2)[rand_int:])
            child_2 = list(np.array(parent_1)[rand_int:]) + list(np.array(parent_2)[:rand_int])
            return child_1, child_2

    def mutate(self):
        """
        Mutation operation
        Picks a candidate, returns the random decisions to create a new candidate
        """
        return model.random_decs(), model.random_decs()

    def penalize_lives(self):
        """
        Type II comparison
        Compares between current frontier and the previous frontier
        if atleast one is better in the current frontier - dont penalize
        """
        for i in xrange(0, model.num_objectives):
            era_old = []
            era_new = []
            for j in xrange(0, len(self.frontier_new)):
                era_old.append(self.frontier[j][i])
                era_new.append(self.frontier_new[j][i])
            if (a12(era_new, era_old) > 0.4):
                return 5
        return -1

    def inbox(self, pebble):
        """
        Helper function to the Hypervolume
        """
        for x in self.frontier_new:
            fun_vector = model.function_value(x, model.num_decisions, model.num_objectives)
            for i in range(model.num_objectives):
                if pebble[i] < fun_vector[i]:
                    return False
        return True

    def hypervolume(self, min_vector, max_vector, n=1000):
        """
        Calculates the Hypervolume in given size
        """
        count = 0.0
        for i in range(n):
            pebble = [random.uniform(min_vector[k], max_vector[k]) for k in range(model.num_objectives)]
            # pebble = [min_vector[k] for k in range(model.num_objectives)]
            if self.inbox(pebble):
                count += 1.0
        return (count / (n * 1.0))

    def fitness(self, population, point, dom_func):
        """
        Evaluate fitness of a point based on the definition in the previous block.
        For example point dominates 5 members of population,
        then fitness of point is 5.
        """
        dominates = 0
        for another in population:
            if dom_func(point, another):
                dominates += 1
        return dominates

    def elitism(self, population, dom_func, size):
        fitnesses = []
        for point in population:
            fitnesses.append((self.fitness(population, point, dom_func), point))
        population = [tup[1] for tup in sorted(fitnesses, reverse=True)]
        return population[:size]

    def run(self, model):

        box = [model.random_decs() for _ in range(self.num_candidates)]

        tests = []

        self.frontier = box
        max_vector, min_vector = self.min_max(box)

        '''Generation'''
        for i in range(self.num_generations):
            say(".")
            #sys.stdout.write("\rGeneration: " + str(i))
            #sys.stdout.flush()
            newbox = []

            '''Candidate Generation'''
            for j in range(self.num_candidates):
                sample = np.random.randint(0, len(self.frontier), size=2)
                child_1 = []
                child_2 = []
                parent_1 = self.frontier[sample[0]]
                parent_2 = self.frontier[sample[1]]

                '''Cross-Over'''
                child_1, child_2 = self.crossover(parent_1, parent_2, child_1, child_2)

                '''Mutation'''
                if random.random() < self.mutation_prob:
                    child_1, child_2 = self.mutate()

                '''New generation'''
                newbox.append(child_1)
                newbox.append(child_2)

            '''Selection of the fitttest'''
            self.frontier_new = []
            self.frontier_new = fastNdom(newbox, self.dominator, self.num_candidates)
            self.lives += self.penalize_lives()

            '''Early termination'''
            if self.lives <= 0:
                break

            box = newbox
            self.frontier = self.frontier_new

        '''Best frontier and hypervolume'''
        hv = self.hypervolume(min_vector, max_vector)

        return [hv, i]


if __name__ == '__main__':

    models = [DTLZ1]
    dom_methods = ['bdom', 'cdom']
    objectives = [2]#, 4, 6, 8]
    decisions = [10]#, 20, 40]
    baseline = 20
    for dom_method in dom_methods:
        for model_type in models:
            print('**Optimizing**', model_type, ' ', dom_method)
            print('--------Baseline Study for :', baseline, 'simulations--------')
            print('\n')
            for decs in decisions:
                for objs in objectives:
                    print('Decisions : ', decs, 'Objectives: ', objs)
                    result = []
                    for i in range(baseline):
                        model = model_type(objs, decs)
                        result.append(GA(model).run(model))
                        say("|")

                    print('Mean Hypervolume: ', np.mean([result[_][0] for _ in range(len(result))]))
                    print('SD   Hypervolume: ', np.std([result[_][0] for _ in range(len(result))]))
                    print('Mean Generations: ', int(np.mean([result[_][1] for _ in range(len(result))])))
                    print('\n')