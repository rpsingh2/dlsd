##Results:
The runtime of a differential evolution algorithm optimizing a genetic algorithm ended up being a lot longer than expected. Even when switching out the standard genetic algorithm for a NSGA-II implementation, the runtime was still quite considerable. With this being said, we found it infeasible to optimize genetic algorithms that optimize each DTLZ model and objective combinations we used previously. 
We instead focused on optimizing GAs that optimized DTLZ5 with 2, 4, 6, and 8 objectives with 10 decisions. From the last homework it was clear to see that DTLZ5 with 2, 4, 6 and 8 all had varying degrees of success when it comes to obtaining maximal hyper volumes. DTLZ5 with 6 and 8 objectives were especially low. We thought it would be interesting to see if we could improve on those results by optimizing NSGA-II and seeing if the modified optimizer gets on average a better hypervolume.

```
SCOTT-KNOTT of results for average HV for GA and DTLZ5 with [2, 4, 6, 8] objs and 10 decisions 
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,    untrained ,      78  ,    27 (---------  *   |      -       ), 0.64,  0.75,  0.78,  0.93,  0.94
   2 ,      trained ,      91  ,    21 (        -------|-    *    --  ), 0.74,  0.87,  0.91,  0.97,  1.01
```
