The data files have been organized in the following way:

-  results_" + problem.name + "-p" + len(population) + "-d" + len(decisions) + "-o" + len(objectives) + "_" + statBox.alg.name + ".datatable"

This file is updated in jmoo_stats_box.update() and contains statistics of how the median values of objectives changes for each generation

- problem.name + "-p" + len(population) + "-d" + len(decisions) + "-o" + len(objectives) + "-dataset.txt"

This file is updated in initialPopulation()

This file contains the population which is then used by all the algorithms as a seed population. The last lines contains

```min(objectives[i]), Medians(objective[i]), max(objective[i]) where i = xrange(0, len(objectives))```


