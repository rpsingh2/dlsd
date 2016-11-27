class Population(object):
    """Represents population - a group of Individuals,
    can merge with another population"""

    def __init__(self):
        self.population = []
        self.fronts = []

    def __len__(self):
        return len(self.population)

    def __iter__(self):
        """Allows for iterating over Individuals"""

        return self.population.__iter__()

    def extend(self, new_individuals):
        """Creates new population that consists of
        old individuals ans new_individuals"""
        self.population.append(new_individuals)

class Individual(object):
    def __init__(self):
        self.rank = None
        self.dominated_solutions = set()
        self.features = None
        self.decisions = None
        self.dominates = None

def fast_nondominated_sort(pop, dominator, k):
    #getting initial fronts
    population = Population()
    for p in pop:
        i = Individual()
        i.decisions = p
        population.extend(i)
    population.fronts = []
    population.fronts.append([])
    for individual in population:
        individual.domination_count = 0
        individual.dominated_solutions = set()

        for other_individual in population:
            if dominator(individual.decisions, other_individual.decisions):
                individual.dominated_solutions.add(other_individual)
            elif dominator(other_individual.decisions, individual.decisions):
                individual.domination_count += 1
        if individual.domination_count == 0:
            population.fronts[0].append(individual)
            individual.rank = 0

    #determine all other fronts
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

    #unpacking and returning
    list = []
    for front in population.fronts:
        for ind in front:
            list.append(ind.decisions)
            if len(list) == k:
                return list