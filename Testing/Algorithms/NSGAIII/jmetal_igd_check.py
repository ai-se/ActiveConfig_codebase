import os
import sys
import inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)

from jmoo_core import *
problem = dtlz1(7, 3)
def readpf(problem):
    filename = "./Testing/PF/" + problem.name.split("_")[0] + "(" + str(len(problem.objectives)) + ")-PF.txt"
    return [[float(num) for num in line.split()] for line in open(filename, "r").readlines()]

def read_file(filename):
    list_objectives = []
    for line in open(filename, "r").readlines():
        if line == "\n": continue
        decision = 7
        objectives = 3
        line = [float(a) for a in line.split()]
        list_objectives.append(line[len(line) - objectives:])
    return list_objectives

resulting_pf = read_file("jmetal_PF")
os.chdir("../../..")  # Since the this file is nested so the working directory has to be changed
from PerformanceMetrics.IGD.IGD_Calculation import IGD

print IGD(resulting_pf, readpf(problem))
