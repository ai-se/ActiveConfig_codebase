import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_core import *
problem = dtlz1(7, 3)


random1_index = 0
random2_index = 0
random3_index = 0
rand_index = 0
random_number = {
    "Random1": [0.041436101832364236],
    "Random2": [0.9216833516490711, 0.7105564251246894, 0.3936375114157197, 0.8594044005638297, 0.2306082711945756, 0.8095587285442903, 0.596937051975804],
    "rand": [0.9968239527467958, 0.23034963558033306],
    "Random3": [0.5713036747163052, 0.2987893101208128]
}

def get_random_number(random_name):
    global rand_index, random1_index, random2_index, random3_index
    number = 0
    if random_name == "Random1":
        number =random_number[random_name][random1_index]
        random1_index += 1
    elif random_name == "Random2":
        number =random_number[random_name][random2_index]
        random2_index += 1
    elif random_name == "Random3":
        number =random_number[random_name][random3_index]
        random3_index += 1
    elif random_name == "rand":
        number =random_number[random_name][rand_index]
        rand_index += 1
    return number

def sbxcrossover2(problem, parent1, parent2):

    EPS = 1.0e-14
    ETA_C_DEFAULT_ = 20.0
    distribution_index = ETA_C_DEFAULT_
    probability = 1
    from copy import copy
    from random import random
    offspring1 = copy(parent1)
    offspring2 = copy(parent2)

    number_of_variables = len(problem.decisions)
    if get_random_number("Random1") <= probability:
        for i in xrange(number_of_variables):
            valuex1 = offspring1.decisionValues[i]
            valuex2 = offspring2.decisionValues[i]
            if get_random_number("Random2") <= 0.5:
                if abs(valuex1 - valuex2) > EPS:
                    if valuex1 < valuex2:
                        y1 = valuex1
                        y2 = valuex2
                    else:
                        y1 = valuex2
                        y2 = valuex1

                    yL = problem.decisions[i].low
                    yU = problem.decisions[i].up
                    rand = get_random_number("rand")
                    beta = 1.0 + (2.0 * (y1 - yL) / (y2 - y1))
                    alpha = 2.0 - beta ** (-1 * (distribution_index + 1.0))

                    if rand <= 1/alpha:
                        betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (distribution_index + 1.0))
                    else:
                        betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (distribution_index + 1.0))

                    c1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
                    beta = 1.0 + (2.0 * (yU - y2) / (y2 - y1))
                    alpha = 2.0 - beta ** -(distribution_index + 1.0)

                    if rand <= (1.0 / alpha):
                        betaq = (rand * alpha) ** (1.0 / (distribution_index + 1.0))
                    else:
                        betaq = ((1.0 / (2.0 - rand * alpha)) ** (1.0 / (distribution_index + 1.0)))

                    c2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))

                    if c1 < yL: c1 = yL
                    if c2 < yL: c2 = yL
                    if c1 > yU: c1 = yU
                    if c2 > yU: c2 = yU

                    if get_random_number("Random3") <= 0.5:
                        offspring1.decisionValues[i] = c2
                        offspring2.decisionValues[i] = c1
                    else:
                        offspring1.decisionValues[i] = c1
                        offspring2.decisionValues[i] = c2
                else:
                    offspring1.decisionValues[i] = valuex1
                    offspring2.decisionValues[i] = valuex2
            else:
                offspring1.decisionValues[i] = valuex2
                offspring2.decisionValues[i] = valuex1

    return offspring1, offspring2



dparent1 = [0.5083748944254394,0.42045196458057343,0.5263802852478026,0.04210630388834613,0.4812361120104276,0.28971621518478874,0.11060003272342767]
dparent2 = [0.20979305263807058,0.7559386704609289,0.733305763188931,0.789917625830216,0.8069206652887255,0.2842634599322028,0.6280687292827736]
parent1 = jmoo_individual(problem, dparent1)
parent2 = jmoo_individual(problem, dparent2)


child1, child2 = sbxcrossover2(problem, parent1, parent2)
print child1.decisionValues
print child2.decisionValues
