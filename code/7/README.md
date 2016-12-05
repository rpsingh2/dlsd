# Exploration of Early Termination using DTLZ model

## Introduction
Within this section you will find a brief overview of the optimizers that were used in this experiment (DE, MWS, SA) as well as some descriptions of statistical comparators.

### Simulated Annealing
Simulated Annealing uses a limited set of memory to determine the best solution given an optimization problem. The only three pieces of information a simulated annealer keeps track of is the newest solution, the best solution and the current solution. Early on within this algorithm random jumps are made in order to explore the Model's landscape. As time progresses, the simulated annealer settles down and begins to look for more stable solutions. This is known as the algorithms cooling factor. This interesting behavior helps the simulated annealer avoid local maxima and minima.
``` 
While has lives and has generations left
  generate candidate soluton
  if candidate solution better than best solution:
    candidate solution saved as best solution
  if candidate solution better than current solution:
    candidate solution saved as current solution
  else if (cooling function returns hot value):
    candidate solution saved as current solution

  if A12 between candidate and current solutions < 56%
    lives - 1
  else:
    lives + 3
```

### Max-WalkSat
Max-WalkSat is similar to Simulated Annealing, but does not have a cooling factor feature. Instead Max-WalkSat has a certain probability of preforming a local search while jumping around the globally. This also helps avoid local maxima and minima by exploring solutions within your current area.

### Differential Evolution
The most complicated and newest algorithm of the bunch. This is a type of Genetic Algorithm, meaning that a population of different solutions are maintained and evolved over time. This difference in the operation of Differential Evolution and the singe objective non-population driven optimizers had to be accounted for.

### Comparison Operators
#### Type 1
#### Type 2: A12
In order to judge the difference in improvement for each optimizer’s current and previous solutions, the A12 small effect comparison was used. A12 is used to determine the overall difference between two sets of numbers. A12 is used to measure the probability that running an algorithm using one set of numbers yields a higher result than running the same algorithm using the second set of numbers. According to Vargha and Delaney, the output from the A12 test can be viewed as such:
-	A12 > 71% represents a large difference
-	A12 > 64% represents a medium difference
-	A12 =< 56% or less represents a small difference
Within the optimizers we implemented, if A12 shows a small difference between the current solution and a candidate solution, the algorithm is assumed to be close to converting to a solution. As such, the optimizer is set to terminate earlier.
#### Type 3: Scott-Knott
The Scott-Knot test is used for clustering results into similar categories. Scott-Knot recursively bi-clusters the output from each of the optimizers into ranks. At each level of ranks, another split is created where the expected values are the most different. Before continuing, Boostrap (random sampling) and A12 are called to check and see if the splits are significantly different.

## Results

```
# Of Eras
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,          mws ,    1000  ,     0 (*              |              ),10.00, 10.00, 10.00, 10.00, 10.00
   1 ,           de ,    1000  ,     0 (*              |              ),10.00, 10.00, 10.00, 10.00, 10.00
   2 ,           sa ,    2600  ,  8900 (     *         |              ),10.00, 10.00, 26.00, 99.00, 99.00

CDOM Between Inital and Final Objectives
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,          mws ,      26  ,    65 (  ---  *    ---|-             ),-0.14,  0.06,  0.26,  0.62,  0.95
   1 ,           sa ,      41  ,    75 (    -     *  --|-----------   ),-0.00,  0.05,  0.41,  0.65,  1.68
   1 ,           de ,      50  ,     8 (           *   |              ), 0.45,  0.46,  0.50,  0.53,  0.55
```

## Threats to Validity

