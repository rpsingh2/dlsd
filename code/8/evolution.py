"""Module with main parts of NSGA-II algorithm.
Contains main loop"""

from utils import NSGA2Utils
from population import Population

class Evolution(object):
    
    def __init__(self, problem, num_of_generations, num_of_individuals, comparitor = "bdom"):
        self.utils = NSGA2Utils(problem, num_of_individuals)

        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals
        self.comparitor = comparitor
    
    def register_on_new_generation(self, fun):
        self.on_generation_finished.append(fun)

    def penalize_lives(self, new_pop, prev_pop):
        """
        Type II comparison
        Compares between current frontier and the previous frontier
        if atleast one is better in the current frontier - dont penalize
        """
        for i in xrange(0, len(new_pop[0].objectives)):
            era_old = []
            era_new = []
            for j in xrange(0, len(new_pop)):
                era_old.append(prev_pop[j].objectives[i])
                era_new.append(new_pop[j].objectives[i])
            from a12 import a12slow
            #print 'a12', a12slow(era_new, era_old)
            if (a12slow(era_new, era_old) > 0.45):
                return 5
        return -1

    def evolve(self):
        lives = 5
        self.population = self.utils.create_initial_population()
        self.utils.fast_nondominated_sort(self.population)
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population)
        returned_population = None

        total_runs = 0

        for i in range(self.num_of_generations):
            total_runs += 1
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            if self.comparitor == "bdom":
                sorted(self.population.fronts[front_num], cmp=self.utils.crowding_operator)
            else:
                sorted(self.population.fronts[front_num], cmp=self.utils.cdom)

            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals-len(new_population)])
            returned_population = self.population

            lives += self.penalize_lives(new_population.population, self.population.population)
            #print lives
            if lives <= 0:
                break

            self.population = new_population
            children = self.utils.create_children(self.population)
            for fun in self.on_generation_finished:
                fun(returned_population, i)

            #hypervolume(returned_population.fronts[0])
        return returned_population.fronts[0], total_runs
                
                
            
            
