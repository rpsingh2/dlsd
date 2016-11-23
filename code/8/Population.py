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