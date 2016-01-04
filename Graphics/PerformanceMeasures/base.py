from __future__ import division
__author__ = 'george'
import sys,os
sys.path.append(os.path.abspath("."))
sys.dont_write_bytecode = True

def get_archive_data(problem, algorithms):

    from DataFrame import ProblemFrame
    data = ProblemFrame(problem, algorithms)
    # print data[-1].get_frontiers()
    # print data[-1].get_extreme_points()
    data.get_reference_point()
    import pdb
    pdb.set_trace()