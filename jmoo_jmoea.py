
"""
##########################################################
### @Author Joe Krall      ###############################
### @copyright see below   ###############################

    This file is part of JMOO,
    Copyright Joe Krall, 2014.

    JMOO is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    JMOO is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with JMOO.  If not, see <http://www.gnu.org/licenses/>.
    
###                        ###############################
##########################################################
"""

"Brief notes"
"Standardized MOEA code for running any MOEA"

from jmoo_algorithms import *
from jmoo_stats_box import *
from jmoo_properties import *
from Algorithms.GALE.Fastmap.Moo import *
# from pylab import *
import jmoo_properties

import os, sys, inspect



def readpf(problem):
    filename = "./Testing/PF/" + problem.name.split("_")[0] + "(" + str(len(problem.objectives)) + ")-PF.txt"
    return [[float(num) for num in line.split()] for line in open(filename, "r").readlines()]

def read_file(problem, filename):
    population = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        decision = 7
        objectives = 3
        line = [float(a) for a in line.split()]
        population.append(jmoo_individual(problem, line[:decision], None))
    return population


def store_values(latestdir, generation_number, population):
    filename = latestdir + "/" + str(generation_number) + ".txt"
    shorten_population = [pop for pop in population if pop.fitness.valid]
    try:
        values = [", ".join(map(str, pop.decisionValues + pop.fitness.fitness)) for pop in shorten_population]
    except:
        import pdb
        pdb.set_trace()
    f = open(filename, 'w')
    for value in values: f.write("%s\n" % value)
    f.close()


def store_values_g4(latestdir, generation_number, population):
    filename = latestdir + "/" + str(generation_number) + ".txt"
    shorten_population = [pop for pop in population if pop.fitness.valid]
    number_of_objectives = len(shorten_population[0].fitness.fitness)
    try:
        values = [", ".join(map(str, pop.decisionValues + pop.fitness.fitness)) for pop in shorten_population]
    except:
        import pdb
        pdb.set_trace()

    try:
        values.extend([", ".join(map(str, pop.decisionValues)) + "," +
                                 ",".join(map(str, ["X" for _ in xrange(number_of_objectives)]))
                       for pop in [pop for pop in population if pop.fitness.valid is False]])
    except:
        import pdb
        pdb.set_trace()
    f = open(filename, 'w')
    for value in values: f.write("%s\n" % value)
    f.close()


def jmoo_evo(problem, algorithm, configurations, toStop = bstop):
    """
    ----------------------------------------------------------------------------
     Inputs:
      -@problem:    a MOP to optimize
      -@algorithm:  the MOEA used to optimize the problem
      -@toStop:     stopping criteria method
    ----------------------------------------------------------------------------
     Summary:
      - Evolve a population for a problem using some algorithm.
      - Return the best generation of that evolution
    ----------------------------------------------------------------------------
     Outputs:
      - A record (statBox) of the best generation of evolution
    ----------------------------------------------------------------------------
    """
    
    # # # # # # # # # # #
    # 1) Initialization #
    # # # # # # # # # # #
    stoppingCriteria = False                             # Just a flag for stopping criteria
    statBox          = jmoo_stats_box(problem,algorithm) # Record keeping device
    gen              = 0                                 # Just a number to track generations
    numeval = 0
    values_to_be_passed = {}
    
    # # # # # # # # # # # # # # # #
    # 2) Load Initial Population  #
    # # # # # # # # # # # # # # # #
    # Though this is not important I am sticking to NSGA3 paper
    # if algorithm.name == "NSGA3":
    #     print "-"*20 + "boom"
    #     jmoo_properties.PSI = jmoo_properties.max_generation[problem.name]
    #     jmoo_properties.MU = population_size[problem.name.split("_")[-1]]

    population = problem.loadInitialPopulation(configurations["Universal"]["Population_Size"])

    assert(len(population) == configurations["Universal"]["Population_Size"]), "The population loaded from the file must be equal to MU"
    from time import time
    old = time()

    # # # # # # # # # # # # # # # #
    # 3.1) Special Initialization #
    # # # # # # # # # # # # # # # #
    if algorithm.initializer is not None:
        # TODO:fix MOEAD
        population, numeval = algorithm.initializer(problem, population, configurations, values_to_be_passed)


    # Generate a folder to store the population
    foldername = "./RawData/PopulationArchives/" + algorithm.name + "_" + problem.name + "/"
    import os
    all_subdirs = [foldername + d for d in os.listdir(foldername) if os.path.isdir(foldername + d)]
    latest_subdir = sorted(all_subdirs, key=os.path.getmtime)[-1]


    # # # # # # # # # # # # # # #
    # 3) Collect Initial Stats  #
    # # # # # # # # # # # # # # #
    statBox.update(population, 0, numeval, initial=True)

    # # # # # # # # # # # # # # #
    # 4) Generational Evolution #
    # # # # # # # # # # # # # # #
    
    while gen < configurations["Universal"]["No_of_Generations"] and stoppingCriteria is False:
        gen+= 1
        print gen, " | ",
        import sys
        sys.stdout.flush()

        # # # # # # # # #
        # 4a) Selection #
        # # # # # # # # #

        problem.referencePoint = statBox.referencePoint
        selectees, evals = algorithm.selector(problem, population, configurations, values_to_be_passed)
        numNewEvals = evals
        old = time()

        # # # # # # # # # #
        # 4b) Adjustment  #
        # # # # # # # # # #
        selectees, evals = algorithm.adjustor(problem, selectees, configurations)
        numNewEvals += evals


        
        # # # # # # # # # # #
        # 4c) Recombination #
        # # # # # # # # # # #

        population, evals = algorithm.recombiner(problem, population, selectees, configurations)


        numNewEvals += evals
        assert(len(population) == configurations["Universal"]["Population_Size"]), \
            "Length of the population should be equal to MU"
        # # # # # # # # # # #
        # 4d) Collect Stats #
        # # # # # # # # # # #
        if algorithm.name == "GALE0" or algorithm.name == "GALE_no_mutation":
            statBox.update(selectees, gen, numNewEvals, population_size=Configurations["Universal"]["Population_Size"])
            store_values(latest_subdir, gen, selectees)
        elif algorithm.name == "GALE4":
            statBox.update(selectees, gen, len(selectees), population_size=Configurations["Universal"]["Population_Size"])
            store_values_g4(latest_subdir, gen, selectees)
        else:
            statBox.update(population, gen, numNewEvals)
            store_values(latest_subdir, gen, population)

        # from PerformanceMetrics.IGD.IGD_Calculation import IGD
        # resulting_pf = [[float(f) for f in individual.fitness.fitness] for individual in statBox.box[-1].population]
        # fitnesses = statBox.box[-1].fitnesses
        # median_fitness = []
        # for i in xrange(len(problem.objectives)):
        #     temp_fitness = [fit[i] for fit in fitnesses]
        #     median_fitness.append(median(temp_fitness))
        # print IGD(resulting_pf, readpf(problem)), median_fitness
            
        # # # # # # # # # # # # # # # # # #
        # 4e) Evaluate Stopping Criteria  #
        # # # # # # # # # # # # # # # # # #
        if algorithm.name != "GALE4":
            stoppingCriteria = toStop(statBox)
        # stoppingCriteria = False

        # assert(len(statBox.box[-1].population) == configurations["Universal"]["Population_Size"]), \
        #     "Length in the statBox should be equal to MU"

    return statBox

