# NSGA-II with CDOM and BDOM + Cuboid distance secondary sorters

## Abstract
NSGA-II is an extremely popular algorithm mused in mutli-objective optimizations problems. NSGA-II is known for its fast selection operator that uses a quick non-domination sort of the frontiers in a population. With this experiment, the results of two types of secondary sorting methods were explored. 
With this setup we tried to explore the difference between using binary domination with cuboid distances and continuous domination as two different types of secondary sorts. Using the DTLZ family of models we were able to obtain results about each of the final populations of points evolved using NSGA-II with each secondary selection method. It turns out neither method has any particualr advantage in terms of impact on hypervolume regardless of the number of objectives used.


## Introduction
### Genetic Algorithm
Genetic Algorithms are a type of optimization technique that maintains a set of candidate solutions known as a population. During each iteration of this algorithm, individual from the population bred with each other and mutated. Then the newly created population is compared to itself and the best out of the new population is saved.

The basic flow is:
*Crossover (create children)
*Mutate (introduce some randomness)
*Evaluate (select fittest)

```
while gen < gens:
    children = []
    for _ in range(pop_size):
        mom = random.choice(population)
        dad = random.choice(population)
        while (mom == dad):
            dad = random.choice(population)
        child = mutate(crossover(mom, dad), mutation_rate)
        if problem.is_valid(child) and child not in population+children:
            children.append(child)
    population += children
    population = elitism(population, pop_size)
    gen += 1
```

### NSGA-II
![alt tag](https://github.com/txt/ase16/blob/master/img/nsgaii.png?raw=true)

Similar to a standard genetic algorithm with a different metric for selection. NSGA-II uses a quick frontier based non-dominated sort to begin with. After the frontiers are sorted, a secondary sort is to the front that contains more samples than is needed for the population. The number of simples needed to maintain the population is kept while the remainder are dropped. The secondary sort mechanic is where the two implementations  of the algorithm differ.

#### Bdom + Cuboid
Cuboid distances are basically the sum of the vertical spaces between the closest candidates to a point. The cuboid distances for each point are compared against one another using binary domination.
![alt tag](https://github.com/txt/ase16/blob/master/img/cuboid.png?raw=true)

Binary domination compares two solutions such that:
1. at least one objective in the first solution is better than any objective in the second solution
2. no objective in the first solution is worse than any objective in the second solution

```
def bdom(one, two):
    dominates = False

    for i in number of objectives:
        if two[i] < one[i]:
            return False
        elif one[i] < two[i]:
            dominates = True

    if dominates: return True
    return False
```

#### Cdom
Continuous domination can be compared to binary domination in that they are both use to compare the dominance of solutions. The difference is that continuous domination determines by how much one point in space dominates another. Instead of returning a binary "yes or no", cdom returns a value indicating how much one list dominates the other. With continuous domination, the differences between two lists are also increased by an exponential factor. As a result, points that dominate a solution by quite a bit stand out more than points that dominate solutions only by a slight margin. This can be used in sorting the population of genetic algorithms.

Candidate solutons that dominate points and have a higher cdom score are more likeley to get kept in a population than those with a lower cdom score.
```
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

    l1 = loss(x, y)
    return l1

```

### Models
All models in this experiment come from the DTLZ family<sup>[1]</sup><sup>[2]</sup>.

#### DTLZ1

![alt tag](http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/dtlz1/images/dtlz1_Formulation.png)

DTLZ1 can be used with any number of objectives and decisions. The pareto frontier for this model is a straight line.

#### DTLZ3

![alt_tag](http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/dtlz3/images/dtlz3_Formulation.png)

DTLZ1 can be used with any number of objectives and decisions. The pareto frontier for this model is a downward sloping curved line.

#### DTLZ5
![alt tag](https://github.com/rpsingh2/fss16rtr/blob/master/code/8/images/DTLZ5.PNG)

DTLZ1 can be used with any number of objectives and decisions. The pareto frontier for this model is also a downward sloping curved line. For some reason, this model became one of the most challenging ones for NSGA-II to fit, especially when dealing with higher numbers of objectives.

#### DTLZ7

![alt tag](http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/dtlz7/images/dtlz7_Formulation.png)

DTLZ7 is a model created in order to test the potential for optimizers to find and maintain several distinct disjointed pareto-optimal solutions. As you can see, when using two objectives, x1 and x2, the pareto-optimal regions are spread out quite a bit. With DTLZ7 it is possible to implement the model using any number of objectives and any number of decisions.

### Result Analysis
#### Hypervolume
Hypervolume is volume with in a pareto frontier. Essentially, hypervolume increases as the pareto frontier approaches closer to its overall goal.<sup>[5]</sup>.

#### A12 (Used With Scott-Knott)
In order to judge the difference in improvement for each optimizer’s current and previous solutions, the A12 small effect comparison was used. A12 is used to determine the overall difference between two sets of numbers. A12 is used to measure the probability that running an algorithm using one set of numbers yields a higher result than running the same algorithm using the second set of numbers. According to Vargha and Delaney, the output from the A12 test can be viewed as such:

*A12 > 71% represents a large difference
*A12 > 64% represents a medium difference
*A12 =< 56% or less represents a small difference

#### Scott-Knott
The Scott-Knot test is used for clustering results into similar categories. Scott-Knot recursively bi-clusters the output from each of the optimizers into ranks. At each level of ranks, another split is created where the expected values are the most different. Before continuing, Boostrap (random sampling) and A12 are called to check and see if the splits are significantly different<sup>[6]</sup>..

This is used in order to determine if there is a significant difference between the resulting hypervolumes for each algorithm.

## Experimental Setup
NSGA-II is applied to DTLZ1, DTLZ3, DTLZ5, DTLZ7 with a variety  of configurations. Each model is tested with 10, 20 and 40 decisions with 2, 4, 6, and 8 objectives. Each permutation of models, the number of decisions and number of objectives are also executed with both Bdom + Cuboid and Cdom as secondary sorting operations. 20 Runs are executed for each permutation of model. After the execution of models, the hypervolume is measured for each optimized solution.

## Results
Each of the results below show an analysis of the hypervolumes generated by NSGA-II given the paramaters under the 'name' column. For example 'dtlz1 8 10 bdom' means NSGA-II optimized the model dtlz1 with 8 objectives and 10 decisions. Each of the hypervolumes are normalized by the number of objectives that the model used. The higher the number, the better the result.

```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 , dtlz5 8 10 bdom ,      64  ,     1 (-*             |              ), 0.63,  0.63,  0.64,  0.65,  0.66
   1 , dtlz5 8 10 cdom ,      64  ,     2 ( *             |              ), 0.62,  0.63,  0.64,  0.64,  0.66
   2 , dtlz5 8 20 cdom ,      72  ,     4 (   - *--       |              ), 0.70,  0.71,  0.73,  0.76,  0.80
   2 , dtlz5 8 20 bdom ,      73  ,     4 (      *        |              ), 0.70,  0.71,  0.74,  0.75,  0.77
   3 , dtlz5 6 10 bdom ,      75  ,     2 (     -*        |              ), 0.74,  0.75,  0.75,  0.78,  0.78
   3 , dtlz5 6 10 cdom ,      77  ,     2 (      -*       |              ), 0.76,  0.77,  0.78,  0.79,  0.80
   4 , dtlz5 6 20 cdom ,      87  ,     5 (          - *- |              ), 0.84,  0.86,  0.89,  0.90,  0.92
   4 , dtlz5 6 20 bdom ,      89  ,     5 (          -- * |              ), 0.83,  0.89,  0.90,  0.92,  0.94
   5 , dtlz5 8 40 bdom ,      92  ,     3 (             *-|              ), 0.88,  0.89,  0.92,  0.93,  0.98
   5 , dtlz5 8 40 cdom ,      91  ,     5 (           -  *|-             ), 0.87,  0.90,  0.93,  0.94,  1.01
   5 , dtlz5 4 10 cdom ,      92  ,     2 (            - *|              ), 0.89,  0.91,  0.92,  0.94,  0.95
   5 , dtlz5 2 10 cdom ,      92  ,     0 (             -*|              ), 0.91,  0.92,  0.92,  0.93,  0.93
   5 , dtlz5 2 40 bdom ,      92  ,     2 (            - *|              ), 0.89,  0.91,  0.93,  0.93,  0.97
   5 , dtlz5 2 10 bdom ,      93  ,     1 (             -*|              ), 0.92,  0.92,  0.93,  0.93,  0.94
   5 , dtlz5 4 10 bdom ,      93  ,     1 (             -*|              ), 0.90,  0.92,  0.93,  0.94,  0.95
   5 , dtlz5 2 40 cdom ,      93  ,     4 (             -*|              ), 0.90,  0.92,  0.94,  0.95,  0.98
   5 , dtlz5 2 20 cdom ,      94  ,     2 (             -*|              ), 0.92,  0.93,  0.94,  0.94,  0.96
   5 , dtlz5 2 20 bdom ,      94  ,     1 (             - *              ), 0.92,  0.93,  0.94,  0.94,  0.96
   6 , dtlz5 4 20 bdom ,      99  ,     3 (               |-*            ), 0.97,  0.99,  1.01,  1.05,  1.07
   6 , dtlz5 4 20 cdom ,     101  ,     5 (               |- *-          ), 0.97,  0.99,  1.02,  1.04,  1.07
   6 , dtlz5 6 40 bdom ,     103  ,     9 (               |-- * ----     ), 0.95,  1.02,  1.04,  1.08,  1.18
   6 , dtlz5 6 40 cdom ,     104  ,    16 (           ----|--  *-------  ), 0.86,  1.02,  1.07,  1.08,  1.23
   7 , dtlz5 4 40 cdom ,     111  ,     2 (               |     -*--     ), 1.10,  1.11,  1.11,  1.13,  1.17
   7 , dtlz5 4 40 bdom ,     115  ,     1 (               |      --*---- ), 1.11,  1.15,  1.16,  1.17,  1.27
```

DTLZ5 turned out to be the only model that produced results that were statisticaly different from oneanother. The output for each of the other models can be found at the bottom of the report.

There appears to be no real difference between hypervolumes of models optimized with bdom + cuboid sorting verses models optimized  with cdom.

What is interesting to see is that as the number of objectives increases, the hypervolume for each optimized model also decreases. When running the experiment, it also appears that as the number of objectives increases, so to does the runtime of NSGA-II.

## Threats to Validity
* Only 20 runs of each model, objective and decision combination were used in order to produce results. More runs of each model may be needed in order to eleminate noise.
* During this experiment, a relatively small number of objectives and decisions were used. Using models with higher numbers of objectives may produce results that show more of a difference between bdom + cuboid and cdom as secondary sorting methods.

## Future Work
* It would be worthwhile  to implement Spread and Intergenerational Distance as a final population fitness measurement in a addition to hypervolume. Perhaps Cdom and Bdom produce different values for Spread and IGD in a way that is not reflected in hypervolume.
* Also changing the number of generations and the population size that NSGA-II has available may help aid in differentiating the results.
* Testing how fast each optimizer can reach a desired hypervolume, spread or intergenerational distance may also lead to interesting results. As the number of objectives and decisions increased, the time it takes for the models to runs increases dramatically. It would be interesting to see how each type of sorting impacts how fast NSGA-II reaches a near-perfect solution. 


## References
[1] http://www.tik.ee.ethz.ch/file/c7c5e610a0c7e26d566a3601e5cce2f4/DTLZ2001a.pdf
[2] http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/
[3] https://github.com/wreszelewski/nsga2/tree/master/nsga2 [refrence for nsga-ii format]
[4] https://ls11-www.cs.uni-dortmund.de/rudolph/hypervolume/start
[5] https://github.com/txt/ase16/blob/master/doc/perform.md
[6] https://github.com/txt/ase16/blob/master/doc/stats.md


## Results Continued:
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 , dtlz1 8 10 bdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz1 8 10 cdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz1 8 20 bdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz1 8 20 cdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz1 8 40 bdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz1 8 40 cdom ,      97  ,     0 (---------------|-------------*), 0.00,  0.97,  0.97,  0.97,  0.97
   1 , dtlz1 6 10 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 6 10 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 6 20 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 6 20 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 6 40 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 6 40 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 4 10 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 4 10 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 4 20 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 4 20 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 4 40 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 4 40 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz1 2 10 bdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz1 2 10 cdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz1 2 20 bdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz1 2 20 cdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz1 2 40 bdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz1 2 40 cdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
```
Results for DTLZ1 are not particularly meaningful. Every algorithm ended up getting a near perfect hypervolume. No decerniable difference between cdom and bdom.

```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 , dtlz3 8 10 bdom ,      97  ,     0 (---------------|-------------*), 0.00,  0.97,  0.97,  0.97,  0.97
   1 , dtlz3 8 10 cdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz3 8 20 bdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz3 8 20 cdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz3 8 40 bdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz3 8 40 cdom ,      97  ,     0 (               |             *), 0.97,  0.97,  0.97,  0.97,  0.97
   1 , dtlz3 6 10 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 6 10 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 6 20 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 6 20 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 6 40 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 6 40 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 4 10 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 4 10 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 4 20 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 4 20 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 4 40 bdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 4 40 cdom ,      98  ,     0 (               |             *), 0.98,  0.98,  0.98,  0.98,  0.98
   1 , dtlz3 2 10 bdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz3 2 10 cdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz3 2 20 bdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz3 2 20 cdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz3 2 40 bdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
   1 , dtlz3 2 40 cdom ,      99  ,     0 (               |             *), 0.99,  0.99,  0.99,  0.99,  0.99
```

Results of dtlz3 ended up being similar to those of dtlz1.


```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 , dtlz7 8 40 cdom ,      85  ,     5 (               |----------*   ), 0.67,  0.85,  0.85,  0.86,  0.87
   1 , dtlz7 8 40 bdom ,      86  ,     3 (               |         - *- ), 0.83,  0.86,  0.87,  0.88,  0.89
   1 , dtlz7 8 20 bdom ,      85  ,    15 (---------------|----------  * ), 0.39,  0.84,  0.88,  0.89,  0.90
   1 , dtlz7 4 20 cdom ,      86  ,    15 (               |-------    *  ), 0.68,  0.79,  0.87,  0.90,  0.90
   1 , dtlz7 6 40 cdom ,      85  ,    26 (        -------|---------   * ), 0.54,  0.83,  0.89,  0.90,  0.91
   1 , dtlz7 8 20 cdom ,      87  ,    16 (               |   -------  * ), 0.72,  0.85,  0.88,  0.89,  0.90
   1 , dtlz7 4 10 bdom ,      88  ,     5 (               |  --------- * ), 0.70,  0.87,  0.88,  0.90,  0.91
   1 , dtlz7 6 40 bdom ,      89  ,     3 (               |         ---* ), 0.84,  0.88,  0.89,  0.89,  0.90
   1 , dtlz7 4 20 bdom ,      89  ,    13 (               | ----------- *), 0.70,  0.88,  0.90,  0.90,  0.90
   1 , dtlz7 8 10 bdom ,      90  ,     1 (               |      ------ *), 0.79,  0.89,  0.90,  0.90,  0.90
   1 , dtlz7 6 20 bdom ,      90  ,     7 (               |   ------    *), 0.73,  0.84,  0.90,  0.90,  0.91
   1 , dtlz7 6 10 bdom ,      90  ,     5 (               |  ---------  *), 0.71,  0.86,  0.90,  0.91,  0.91
   1 , dtlz7 6 20 cdom ,      90  ,     1 (               |           - *), 0.88,  0.89,  0.90,  0.91,  0.91
   1 , dtlz7 8 10 cdom ,      90  ,     1 (               |            -*), 0.88,  0.90,  0.90,  0.90,  0.90
   1 , dtlz7 6 10 cdom ,      90  ,     1 (               |            -*), 0.89,  0.90,  0.90,  0.91,  0.91
   1 , dtlz7 4 40 bdom ,      90  ,     4 (               |   ----------*), 0.74,  0.90,  0.90,  0.90,  0.91
   1 , dtlz7 4 40 cdom ,      90  ,     4 (               |           --*), 0.87,  0.90,  0.90,  0.91,  0.91
   1 , dtlz7 4 10 cdom ,      90  ,     2 (               |            -*), 0.89,  0.89,  0.90,  0.91,  0.91
   1 , dtlz7 2 10 bdom ,      91  ,     0 (               |             *), 0.91,  0.91,  0.91,  0.91,  0.91
   1 , dtlz7 2 40 cdom ,      91  ,     0 (               |             *), 0.90,  0.91,  0.91,  0.91,  0.91
   1 , dtlz7 2 20 cdom ,      91  ,     0 (               |             *), 0.90,  0.91,  0.91,  0.91,  0.91
   1 , dtlz7 2 20 bdom ,      91  ,     0 (               |             *), 0.91,  0.91,  0.91,  0.91,  0.91
   1 , dtlz7 2 10 cdom ,      91  ,     0 (               |             *), 0.91,  0.91,  0.91,  0.91,  0.91
   1 , dtlz7 2 40 bdom ,      91  ,     0 (               |             *), 0.91,  0.91,  0.91,  0.91,  0.91
```

Dtlz7 ended up having more variety in hypervolume between low objective vs high objective models. No splits according to Scott-Knott.
