import sys
maxVal = sys.maxint
minVal = -maxVal

def eucledian(one, two):
  """
  Compute Eucledian Distance between
  2 vectors. We assume the input vectors
  are normalized.
  :param one: Vector 1
  :param two: Vector 2
  :return:
  """
  # TODO 4: Code up the eucledian distance. https://en.wikipedia.org/wiki/Euclidean_distance
  return (sum([(o-t) ** 2 for o,t in zip(one, two)]) / len(one)) ** 0.5

def sort_solutions(solutions):
    """
    Sort a list of list before computing spread
    """
    def sorter(lst):
        m = len(lst)
        weights = reversed([10 ** i for i in xrange(m)])
        return sum([element * weight for element, weight in zip(lst, weights)])
    return sorted(solutions, key=sorter)


def closest(one, many):
    import sys
    min_dist = sys.maxint
    closest_point = None
    for this in many:
        dist = eucledian(this, one)
        if dist < min_dist:
            min_dist = dist
            closest_point = this
    return min_dist, closest_point


def make_reference(problem, *fronts):
    """
    Make a reference set comparing all the fronts.
    Here the comparison we use is bdom. It can
    be altered to use cdom as well
    """
    retain_size = len(fronts[0])
    reference = []
    for front in fronts:
        reference += front

    def bdom(one, two):
        """
        Return True if 'one' dominates 'two'
        else return False
        :param one - [pt1_obj1, pt1_obj2, pt1_obj3, pt1_obj4]
        :param two - [pt2_obj1, pt2_obj2, pt2_obj3, pt2_obj4]
        """
        dominates = False
        for i, obj in enumerate(problem.objectives):
            def gt(a, b): return a > b
            def lt(a, b): return a < b
            better = lt if obj.do_minimize else gt
            # TODO 3: Use the varaibles declared above to check if one dominates two
            if better(one[i], two[i]):
                dominates = True
            elif one[i] != two[i]:
                return False
        return dominates

    def fitness(one, dom):
        return len([1 for another in reference if dom(one, another)])

    fitnesses = []
    for point in reference:
        fitnesses.append((fitness(point, bdom), point))
    reference = [tup[1] for tup in sorted(fitnesses, reverse=True)]
    return reference[:retain_size]

def normalize(problem, points):
  """
  Normalize all the objectives
  in each point and return them
  """
  all_objs = []
  for point in points:
    objs = []
    for i, o in enumerate(problem.function_value(point, problem.num_decisions, problem.num_objectives)):
      high, low = maxVal, minVal
      # TODO 2: Normalize 'o' between 'low' and 'high'; Then add the normalized value to 'objs'
      if high == low: objs.append(0); continue;
      objs.append((o - low)/(high - low))
    all_objs.append(objs)
  return all_objs

def spread(obtained, ideals):
  """
  Calculate the spread (a.k.a diversity)
  for a set of solutions
  """
  s_obtained = sort_solutions(obtained)
  s_ideals = sort_solutions(ideals)
  d_f = closest(s_ideals[0], s_obtained)[0]
  d_l = closest(s_ideals[-1], s_obtained)[0]
  n = len(s_ideals)
  distances = []
  for i in range(len(s_obtained)-1):
    distances.append(eucledian(s_obtained[i], s_obtained[i+1]))
  d_bar = sum(distances)/len(distances)
  # TODO 5: Compute the value of spread using the definition defined in the previous cell.
  d_sum = sum([abs(d_i - d_bar) for d_i in distances])
  delta = (d_f + d_l + d_sum) / (d_f + d_l + (n-1) * d_bar)

def igd(obtained, ideals):
    """
    Compute the IGD for a
    set of solutions
    :param obtained: Obtained pareto front
    :param ideals: Ideal pareto front
    :return:
    """
    # TODO 6: Compute the value of IGD using the definition defined in the previous cell.


    igd_val = sum([closest(ideal, obtained)[0] for ideal in ideals]) / len(ideals)
    return igd_val