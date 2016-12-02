import random
import functools

from population import Population
from stats import a12

from hypervolume import *
from stats import rdivDemo as sk

def hv(population, num_objectives):
    referencePoint = [11 for _ in range(num_objectives)]
    hv = InnerHyperVolume(referencePoint)

    volume = hv.compute(individual.objectives for individual in population)
    return volume

def norm_hypervol(hv, obj):
    exp = 1 if obj == 2 else obj / 2
    return hv / (122 ** exp)


class NSGAII(object):
    def __init__(self, problem, num_of_generations, num_of_individuals, comparitor="bdom"):
        self.population = None
        self.problem = problem

        self.num_of_generations = num_of_generations
        self.num_of_individuals = num_of_individuals
        self.mutation_strength = 0.3
        self.comparitor = comparitor

        self.hypervolume = 0

    def fast_nondominated_sort(self, population):
        population.fronts = []
        population.fronts.append([])
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = set()

            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.add(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                population.fronts[0].append(individual)
                individual.rank = 0
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    def __sort_objective(self, val1, val2, m):
        return cmp(val1.objectives[m], val2.objectives[m])

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front = sorted(front, cmp=functools.partial(self.__sort_objective, m=m))
                front[0].crowding_distance = self.problem.max_objectives[m]
                front[solutions_num - 1].crowding_distance = self.problem.max_objectives[m]
                for index, value in enumerate(front[1:solutions_num - 1]):
                    front[index].crowding_distance = (front[index + 1].crowding_distance - front[
                        index - 1].crowding_distance) / (
                                                         self.problem.max_objectives[m] - self.problem.min_objectives[
                                                             m])

    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (
                            individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1

    def cdom(self, x, y):
        def expLoss(w, x1, y1, n):
            return -1 * (w * (x1 - y1) / n)

        def loss(x, y):
            losses = []
            n = min(len(x), len(y))
            for obj in range(n):
                x1, y1 = x[obj], y[obj]
                losses += [expLoss(-1, x1, y1, n)]
            return sum(losses) / n

        x = x.objectives[:]
        y = y.objectives[:]
        l1 = loss(x, y)
        return int(l1)

    def create_initial_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.problem.generateIndividual()
            self.problem.calculate_objectives(individual)
            population.population.append(individual)

        return population

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1.features == parent2.features:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1, 1)
            self.__mutate(child2, 1)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def __crossover(self, individual1, individual2):
        child1 = self.problem.generateIndividual()
        child2 = self.problem.generateIndividual()
        genes_indexes = range(len(child1.features))
        half_genes_indexes = random.sample(genes_indexes, 1)
        for i in genes_indexes:
            if i in half_genes_indexes:
                child1.features[i] = individual2.features[i]
                child2.features[i] = individual1.features[i]
            else:
                child1.features[i] = individual1.features[i]
                child2.features[i] = individual2.features[i]
        return child1, child2

    def __mutate(self, child, num_mutations):
        genes_to_mutate = random.sample(range(0, len(child.features)), num_mutations)
        for gene in genes_to_mutate:
            child.features[gene] = child.features[
                                       gene] - self.mutation_strength / 2 + random.random() * self.mutation_strength
            if child.features[gene] < 0:
                child.features[gene] = 0
            elif child.features[gene] > 1:
                child.features[gene] = 1

    def __tournament(self, population):
        participants = random.sample(population, 2)
        best = None
        for participant in participants:
            if best is None or self.crowding_operator(participant, best) == 1:
                best = participant

        return best

    def register_on_new_generation(self, fun):
        self.on_generation_finished.append(fun)

    def penalize_lives(self, new_pop, prev_pop):
        for i in xrange(0, len(new_pop[0].objectives)):
            era_old = []
            era_new = []
            for j in xrange(0, len(new_pop)):
                era_old.append(prev_pop[j].objectives[i])
                era_new.append(new_pop[j].objectives[i])
            if (a12(era_new, era_old) > 0.56):
                return 5
        return -1

    def run(self):
        lives = 5

        self.population = self.create_initial_population()
        self.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.calculate_crowding_distance(front)
        children = self.create_children(self.population)
        returned_population = None

        total_runs = 0

        for i in range(self.num_of_generations):
            total_runs += 1
            self.population.extend(children)
            self.fast_nondominated_sort(self.population)

            new_population = Population()
            front_num = 0

            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            if self.comparitor == "bdom":
                sorted(self.population.fronts[front_num], cmp=self.crowding_operator)
            else:
                sorted(self.population.fronts[front_num], cmp=self.cdom)

            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])
            returned_population = self.population

            self.population = new_population
            children = self.create_children(self.population)

            self.hypervolume = norm_hypervol(hv(self.population.population, self.problem.num_objectives), self.problem.num_objectives)
            if self.hypervolume >= 0.99:
                #print "volbreak"
                break

        return self.hypervolume, total_runs
