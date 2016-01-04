import os, sys, inspect
cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe()))[0], "../../..")))
if cmd_subfolder not in sys.path:
    sys.path.insert(0, cmd_subfolder)
from jmoo_core import *
problem = dtlz1(7, 3)

pop1 = [0.543649202577545,0.07986632268356297,0.0859936264195924,0.04677927473161847,0.8129428202477043,0.9567637445535091,0.15907230605632616]

print problem.evaluate(pop1)