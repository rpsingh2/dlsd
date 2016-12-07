# Hyper parameter optimization (fun 😒😓) 
## Abstract
Over the course of this semester we have learned a lot about how optimizers can help find solutions to many kinds of complex models. We also learned that determining what parameters to use on an optimizer can also impact the optimizer’s performance.

Naturally, the next step is to use an optimizer to optimize an optimizer. With During this experiment, we decided to use Differential Evolution in order to maximize the hypervolume produced by an instance of NSGA-II while using the model DTLZ5.

Overall we received promising results with respect to an improvement in average hypervolume.

## Introduction
This section provides a general overview of some of the teh

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

NSGA-II was used instead of a generic genetic al for this problem since NSGA-II has a faster runtime<sup>[1]</sup>. 

### Differential Evolution
This is a type of Genetic Algorithm, meaning that a population of different solutions are maintained and evolved over time. This difference in the operation of Differential Evolution and the singe objective non-population driven optimizers had to be accounted for.

Differential Evolution uses a different mutator method compared to a standard genetic algorithm. DE mutates an individual's decision such that:
new = X + F*(Y - Z)
Where X, Y and Z are other random individual's decisions and F is a set constant.

```
While has generations left and has lives
	Mutated population = Mutate(population)
	Return n fittest from population
	Save new population	
```

### Performance Measures
#### Hypervolume
Hypervolume is area that the pareto frontier contains. Essentially the size of the area that can contain non-pareto solutions. The better the hypervolume, the greater the area explored and the better the pareto solutions.<sup>[2]</sup>.

#### A12 (Used With Scott-Knott)
In order to judge the difference in improvement for each optimizer’s current and previous solutions, the A12 small effect comparison was used. A12 is used to determine the overall difference between two sets of numbers. A12 is used to measure the probability that running an algorithm using one set of numbers yields a higher result than running the same algorithm using the second set of numbers. According to Vargha and Delaney, the output from the A12 test can be viewed as such:


*A12 > 71% represents a large difference
*A12 > 64% represents a medium difference
*A12 =< 56% or less represents a small difference

#### Scott-Knott
The Scott-Knot test is used for clustering results into similar categories. Scott-Knot recursively bi-clusters the output from each of the optimizers into ranks. At each level of ranks, another split is created where the expected values are the most different. Before continuing, Boostrap (random sampling) and A12 are called to check and see if the splits are significantly different<sup>[3]</sup>.


This is used in order to determine if there is a significant difference between the resulting hypervolumes for each algorithm.

## Experimental Setup
NSGA-II is applied to DTLZ1, DTLZ3, DTLZ5, DTLZ7 with a variety  of configurations. Each model is tested with 10, 20 and 40 decisions with 2, 4, 6, and 8 objectives. Each permutation of models, the number of decisions and number of objectives are also executed with both Bdom + Cuboid and Cdom as secondary sorting operations. 20 Runs are executed for each permutation of model. After the execution of models, the hypervolume is measured for each optimized solution.

##Experimental Setup
The runtime of a differential evolution algorithm optimizing a genetic algorithm ended up being a lot longer than expected. We thought of swapping out a standard genetic algorithm for NSGA-II since the later is supposed to be faster than a GA <sup>[1]</sup>. Even when switching out the standard genetic algorithm for a NSGA-II implementation, the runtime was still quite considerable. With this being said, we found it infeasible to optimize genetic algorithms that optimize each DTLZ model and objective combinations we used previously. 

We instead focused on optimizing GAs that optimized DTLZ5 with 2, 4, 6, and 8 objectives with 10 decisions. From the last homework it was clear to see that DTLZ5 with 2, 4, 6 and 8 all had varying degrees of success when it comes to obtaining maximal hyper volumes. DTLZ5 with 6 and 8 objectives were especially low. We thought it would be interesting to see if we could improve on those results by optimizing NSGA-II and seeing if the modified optimizer gets on average a better hypervolume.

Our DE that optimizes NSGA-II has the following parameters:
* 30% Crossover Rate
* 75% Mutation Factor
* DE/rand/1 Mutation Scheme
* Population: 10
* Generations: 5
[Population and Generations were both set to low values. High values increase the runtime far too much]

##Results:

```
SCOTT-KNOTT of results for average HV for GA and DTLZ5 with [2, 4, 6, 8] objs and 10 decisions 
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,      untuned ,      78  ,    27 (---------  *   |      -       ), 0.64,  0.75,  0.78,  0.93,  0.94
   2 ,        tuned ,      91  ,    21 (        -------|-    *    --  ), 0.74,  0.87,  0.91,  0.97,  1.01
```

The results show that on average the median hyperovlume produced by the trained NSGA-II optimizer is greater than the average to that of the untrained classifier. Also with the trained optimizers, the highest hypervolume obtained is greater than the highest hypervolume obtained by the untrained NSGA-II algorithm. Even with a low population and number of generations, the DE overall improved the average hypervolume for NSGA-II.

```
Final Trained NSGA-II paramaters

          name ,    med   ,  iqr 
------------------------------------------------
  # Population ,    7100  ,  4500 (  -----        *   ----       ),28.00, 46.00, 73.00, 85.00, 100.00

          name ,    med   ,  iqr 
----------------------------------
 # Generations ,    4400  ,  1900 (       -----  *|  ------      ),27.00, 39.00, 44.00, 56.00, 71.00
   
          name ,    med   ,  iqr 
----------------------------------------------------
 Mutation Rate ,      64  ,    53 (        ---    |   *      --- ), 0.27,  0.38,  0.64,  0.90,  1.00
```

The second set of results depict the optimal settings for tuned NSGA-II. The population size runs the gambit from close to the minimum population of 20 to the max of 100. In general, the spread above and below the mean are pretty even. The number of generations ended up staying around the mean of 44 with less overall variance in data when compared to the population size. The mutation rate ended up being quite high. The mean mutation rate ended up being 64%.

Threats to Validity:
* All combinations of DTLZ as well as a variety of sizes for both number of objectives and decisions should be tested in order to see if the current findings hold true for the other models as well.
* In addition to hypervolume, spread and intergenerational distance can also be considered for optimizing a genetic algorithm.
* Due to time constraints, a relatively small population and number of generations were used for the differential evolution optimizer. With a larger population and greater number of generations the average hypervolume may improve even more.

Future Work:
* From the results it appears that a higher Mutation Rate for a GA may have beneficial effect in terms of maximizing the hypervolume. 
..* Implementing some sort of simulated annealing inspired mutation rate where it is higher at the start of execution, and gets more tame over time
..*It would be interesting to see if a higher Mutation Rate is beneficial in most models or if this is just one exception.
* Implementing code in a threaded fashion to allow for quicker runtimes is really a must. Waiting for even a relatively small run of the DE is painfully slow.
* Implementing all other DTLZ models and comparing the results could lead to interesting conclusions.

Refrences:
[1] https://github.com/txt/ase16/blob/master/doc/nsga2spea2.md
[2]  https://github.com/txt/ase16/blob/master/doc/perform.md
[3] https://github.com/txt/ase16/blob/master/doc/stats.md
[4]
