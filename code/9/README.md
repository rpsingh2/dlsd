##Results:
The runtime of a differential evolution algorithm optimizing a genetic algorithm ended up being a lot longer than expected. We thought of swapping out a standard genetic algorithm for NSGA-II since the later is supposed to be faster than a GA [1]. Even when switching out the standard genetic algorithm for a NSGA-II implementation, the runtime was still quite considerable. With this being said, we found it infeasible to optimize genetic algorithms that optimize each DTLZ model and objective combinations we used previously. 

We instead focused on optimizing GAs that optimized DTLZ5 with 2, 4, 6, and 8 objectives with 10 decisions. From the last homework it was clear to see that DTLZ5 with 2, 4, 6 and 8 all had varying degrees of success when it comes to obtaining maximal hyper volumes. DTLZ5 with 6 and 8 objectives were especially low. We thought it would be interesting to see if we could improve on those results by optimizing NSGA-II and seeing if the modified optimizer gets on average a better hypervolume.

```
SCOTT-KNOTT of results for average HV for GA and DTLZ5 with [2, 4, 6, 8] objs and 10 decisions 
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,      untuned ,      78  ,    27 (---------  *   |      -       ), 0.64,  0.75,  0.78,  0.93,  0.94
   2 ,        tuned ,      91  ,    21 (        -------|-    *    --  ), 0.74,  0.87,  0.91,  0.97,  1.01
```

The untrained NSGA-II = [Population Size = 50, Generations = 50, Mutation Rate = 0.3]
The average Trained NSGA-II = [Population Size = 50, Generations = 50, Mutation Rate = 0.3]

The results show that on average the median hyperovlume produced by the trained NSGA-II optimizer is greater than the average to that of the untrained classifier. Also with the trained optimizers, the highest hypervolume obtained is greater than the highest hypervolume obtained by the untrained NSGA-II algorithm.

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
All combinations of DTLZ as well as a variety of sizes for both number of objectives and decisions should be tested in order to see if the current findings hold true for the other models as well.
In addition to hypervolume, spread and intergenerational distance can also be considered for optimizing a genetic algorithm.
Due to time constraints, a relatively small population and number of generations were used for the differential evolution optimizer. With a larger population and greater number of generations the average hypervolume may improve even more.

Refrences:
[1] https://github.com/txt/ase16/blob/master/doc/nsga2spea2.md
