
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
"Report tool for keeping track of stats during MOEAs"

import math
import jmoo_algorithms
from jmoo_individual import *
import jmoo_properties
from utility import *
IGDMEASURE = False
import os, inspect, sys
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "Techniques")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from PerformanceMetrics.IGD.IGD_Calculation import IGD

def readpf(problem):
    # print problem.name.split("_")[0]
    filename = "./PF/" + problem.name.split("_")[0] + "(" + str(len(problem.objectives)) + ")-PF.txt"
    f = open(filename, "r")
    true_PF = []
    for line in f:
        temp = []
        for x in line.split():
            temp.append(float(x))
        true_PF.append(temp)
    return true_PF


class jmoo_stats:
    "A single stat box - a simple record"
    def __init__(stats, population, fitnesses, fitnessMedians, fitnessSpreads, numEval, gen, IBD, IBS, changes):
        stats.population = population
        stats.fitnesses = fitnesses
        stats.fitnessMedians = fitnessMedians
        stats.fitnessSpreads = fitnessSpreads
        stats.numEval = numEval
        stats.gen = gen
        stats.IBD = IBD
        stats.IBS = IBS
        stats.changes = changes
        
     
          
class jmoo_stats_box:
    "Management of one stat box per generation"
    def __init__(statBox, problem, alg, foam=None):
        statBox.problem = problem
        statBox.numEval = 0
        statBox.box = [0]
        statBox.alg = alg
        statBox.foam = [{} for o in problem.objectives]
        statBox.bests = [100.0 for o in problem.objectives]
        statBox.bests_actuals = [0 for o in problem.objectives]
        statBox.lives = 3
        statBox.reference_point_for_hypervolume = None
    
    def update(statBox, population, gen, num_new_evals, initial = False, population_size=None, printOption=True):
        "add a stat box - compute the statistics first"

        # Find a file name to write the stats to
        if (statBox.alg.name == "GALE0" or statBox.alg.name == "GALE_no_mutation") and population_size is not None:
            filename = "Data/results_"+statBox.problem.name + "-p" + str(population_size) + "-d" + \
                   str(len(statBox.problem.decisions)) + "-o" + str(len(statBox.problem.objectives))+\
                   "_"+statBox.alg.name+".datatable"
        else:
            filename = "Data/results_"+statBox.problem.name + "-p" + str(len(population)) + "-d" + \
                       str(len(statBox.problem.decisions)) + "-o" + str(len(statBox.problem.objectives))+\
                       "_"+statBox.alg.name+".datatable"

        fa = open(filename, 'a')

        # Update Number of Evaluations
        statBox.numEval += num_new_evals

        # population represents on the individuals which have been evaluated
        shorten_population = [pop for pop in population if pop.fitness.valid]
        objectives = [individual.fitness.fitness for individual in shorten_population]
        # Split Columns into Lists
        objective_columns = [[objective[i] for objective in objectives] for i, obj in enumerate(statBox.problem.objectives)]
        # Calculate Medians of objective scores
        objective_medians = [median(fitCol) for fitCol in objective_columns]
        # Calculate IQR of objective scores
        objective_iqr = [spread(fitCol) for fitCol in objective_columns]
        
        # Initialize Reference Point on Initial Run
        if initial is True:
            statBox.referencePoint = [o.med for o in statBox.problem.objectives]
            statBox.reference_point_for_hypervolume = [o.up for o in statBox.problem.objectives]


        # Calculate IBD & IBS
        # Finding min and max for each objectives
        norms = [[min(objective_columns[i]+[statBox.referencePoint[i]]), max(objective_columns[i]+[statBox.referencePoint[i]])] for i,obj in enumerate(statBox.problem.objectives)]

        lossInQualities = [{"qual": loss_in_quality(statBox.problem, [statBox.referencePoint], fit, norms), "index": i} for i,fit in enumerate(objectives)]
        lossInQualities.sort(key=lambda(r): r["qual"])
        if len(objectives) > 0: 
            best_fitness = objectives[lossInQualities[0]["index"]]
        else:
            best_fitness = objective_medians
        lossInQualities = [item["qual"] for item in lossInQualities]

        IBD = median(lossInQualities)
        IBS = spread(lossInQualities)

        if initial is True:
            IBD = 1.0
            statBox.referenceIBD = 1.0
        
        changes = []
        # Print Option
        if printOption is True:
            outString = ""
            
            if initial:
                outString += str(statBox.numEval) + ","
                for med, spr, initmed, obj, o in zip(statBox.referencePoint, [0 for x in statBox.problem.objectives],
                                                 statBox.referencePoint, statBox.problem.objectives,
                                                 range(len(statBox.problem.objectives))):
                    change = percentChange(med, initmed, obj.lismore, obj.low, obj.up)
                    changes.append(float(change.strip("%")))
                    statBox.bests[o] = changes[-1]
                    statBox.bests_actuals[o] = med
                    outString += str("%8.4f" % med) + "," + change + "," + str("%8.4f" % spr) + ","
                    if statBox.numEval in statBox.foam[o]: statBox.foam[o][statBox.numEval].append(change)
                    else: statBox.foam[o][statBox.numEval] = [change]
                outString += str("%8.4f" % IBD) + "," + percentChange(statBox.referenceIBD, statBox.referenceIBD, True, 0, 1) + "," + str("%8.4f" % IBS)
            else:
                outString += str(statBox.numEval) + ","
                for med, spr, initmed, obj, o in zip(best_fitness, objective_iqr, statBox.referencePoint,
                                                 statBox.problem.objectives, range(len(statBox.problem.objectives))):
                    change = percentChange(med, initmed, obj.lismore, obj.low, obj.up)
                    changes.append(float(change.strip("%")))
                    if changes[-1] < statBox.bests[o]: 
                        statBox.bests[o] = changes[-1]
                        statBox.bests_actuals[o] = med
                    outString += str("%8.4f" % med) + "," + change + "," + str("%8.4f" % spr) + ","
                    if statBox.numEval in statBox.foam[o]: statBox.foam[o][statBox.numEval].append(change)
                    else: statBox.foam[o][statBox.numEval] = [change]
                outString += str("%8.4f" % IBD) + "," + percentChange(IBD, statBox.referenceIBD, True, 0, 1) + "," + str("%8.4f" % IBS)
            fa.write(outString + "\n")
        
            
        # Add Stat to the Stat Box
        trunk = []
        for i,pop in enumerate(shorten_population):
            trunk.append(jmoo_individual(statBox.problem, pop.decisionValues, pop.fitness.fitness))
        statBox.box[-1] = jmoo_stats(trunk, objectives, best_fitness, objective_iqr, statBox.numEval, gen, IBD, IBS, changes)
        fa.close()
###########
### Utility Functions
###########

def percentChange(new, old, lismore, low, up):
    # print "old: ", old
    # print "new: ", new
    return str("%1.1f" % changeFromOld(new, old, lismore, low, up)) + "%"

def changeFromOld(new, old, lismore, low, up):
    if new < 0 or old < 0: 
        ourlismore = not lismore
        new = abs(new)
        old = abs(old)
    else: ourlismore = lismore
    # if new == 0 or old == 0: return 0 if ourlprintismore else 110
    new = normalize(new, low, up)
    old = normalize(old, low, up)
    if old == 0: x = 0
    else: x = (new/float(old))
    if x == 0: 
        if ourlismore: return 0
        else: return 1
    else: return 100.0*x**(1 if ourlismore else -1)
def median(list):
    return getPercentile(list, 50)

def spread(list):
    return getPercentile(list, 75) - getPercentile(list, 25)

def getPercentile(list, percentile):
        if len(list) == 0: return 0
        #sort the list
        list.sort()
        
        k = (len(list) - 1) * (percentile/100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            val = list[int(k)]
        else:
            d0 = list[int(f)] * (c-k)
            d1 = list[int(c)] * (k-f)
            val = d0+d1
        return val

def normalize(x, min, max):
    tmp = float((x - min)) / \
                (max - min + 0.000001) 
    if   tmp > 1 : return 1
    elif tmp < 0 : return 0
    else         : return tmp 
    
def loss_in_quality(problem, pop, fit1, norms):
    "Loss in Quality Indicator"
    weights = [-1 if o.lismore else +1 for o in problem.objectives]    
    k = len(weights)
    
    # Calculate the loss in quality of removing fit1 from the population
    F = []
    for X2 in pop:
        F.append(-k/(sum([-math.exp(-w*(normalize(p2,n[0],n[1]) - normalize(p1,n[0],n[1]))/k) for w,p1,p2,n in zip(weights,fit1,X2,norms)])))
    F1 = sum(F)
    
    return F1
