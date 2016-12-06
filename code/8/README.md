# NSGA-II with CDOM and BDOM + Cuboid distance secondary sorters

## Abstract
This experiment explores the difference between NSGA-II with different secondary sort operators. With this setup we tried to explore the diffrence between using binary domination with cuboid distances and continuous domination as two different types of selection operators. It turns out that both seem about the same in terms of impact on hypervolume reguardless of the number of objectives used.

## Introduction
### Genetic Algorithm
Genetic Algorithms are a type of optimization technique that keep a collection as solutions known as a population. During each iteration of this algorithm, the populations decisions are bred with eachother and mutated. Then the newly created population is compared to itself and the best out of the new population is saved.

### NSGA-II
![alt tag](https://github.com/txt/ase16/blob/master/img/nsgaii.png?raw=true)
Similar to a standard genetic algorithm with a different metric for selection. NSGA-II uses a quick frontier based non-dominated sort to begin with. After the frontiers are sorted, a secondary sort is to the front that contains more samples than is neccicary for the population. The number of simples needed to maintain the population is kept while the remainder are dropped. The secondary sort mechanic is where the two implementions of the algorithm differ.

#### Bdom + Cuboid
Cuboid distances is basically the sum of the verticle spaces between the closest candidates to a point. 
![alt tag](https://github.com/txt/ase16/blob/master/img/cuboid.png?raw=true)

#### Cdom

### Models
#### DTLZ1
#### DTLZ3
#### DTLZ5
#### DTLZ7
![alt tag](http://people.ee.ethz.ch/~sop/download/supplementary/testproblems/dtlz7/images/dtlz7_Formulation.png)
DTLZ7 is a model created in order to test the potential for optimizers to find and maintain several distinct disjointed pareto-optimal solutions. As you can see, when using two objectives, x1 and x2, the pareto-optimal regions are spread out quite a bit. With DTLZ7 it is possible to implement the model using any number of objectives and any number of decisions.

### Result Analysis
#### Hypervolume
Hypervolume is area that the pareto frontier contains. Essentially the size of the area that can contain non-pareto solutions. The better the hypervolume, the greater the area explored and the better the pareto solutions.

#### Scott-Knott
The Scott-Knot test is used for clustering results into similar categories. Scott-Knot recursively bi-clusters the output from each of the optimizers into ranks. At each level of ranks, another split is created where the expected values are the most different. Before continuing, Boostrap (random sampling) and A12 are called to check and see if the splits are significantly different.

This is used in order to determine if there is a significant difference between the resulting hypervolumes for each algorithm.

## Experimental Setup
NSGA-II is applied to DTLZ1, DTLZ3, DTLZ5, DTLZ7 with a veriety of configurations. Each model is testd with 10, 20 and 40 decisions with 2, 4, 6, and 8 objectives. Each permutation of models, the number of decisions and number of objectives are also executed with both Bdom + Cuboid and Cdom as secondary sorting operations. 20 Runs are executed for each permutation of model. After the execution of models, the hypervolume is measured for each optimized solution.

## Results

## Threats to Validity

## Future Work

## Refrences
