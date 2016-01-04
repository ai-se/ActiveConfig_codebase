
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
"Property File.  Defines default settings."

from jmoo_algorithms import *
from jmoo_problems import *

from Problems.CPM.cpm_reduction import *



# JMOO Experimental Definitions
algorithms = [
              jmoo_GALE(),
              jmoo_NSGAII(),
              jmoo_DE()
              ]

problems =[
    cpm_apache_training_reduction(treatment=None),
    cpm_X264(treatment=None),
    cpm_SQL(treatment=None),
    cpm_LLVM(treatment=None),
    cpm_BDBJ(treatment=None),
    cpm_BDBC(treatment=None)
]

build_new_pop = False                                       # Whether or not to rebuild the initial population

Configurations = {
    "Universal": {
        "Repeats" : 1,
        "Population_Size" : 100,
        "No_of_Generations" : 20
    },
    "GALE": {
        "GAMMA" : 0.15,  #Constrained Mutation Parameter
        "EPSILON" : 1.00,  #Continuous Domination Parameter
        "LAMBDA" :  3,     #Number of lives for bstop
        "DELTA"  : 3       # Accelerator that increases mutation size
    },
    "DE": {
        "F" : 0.75, # extrapolate amount
        "CF" : 0.3, # prob of cross over
    },
}


# File Names
DATA_PREFIX        = "Data/"
DEFECT_PREDICT_PREFIX = "defect_prediction/"
VERSION_SPACE_PREFIX = "version_space/"

"decision bin tables are a list of decisions and objective scores for a certain model"
DECISION_BIN_TABLE = "decision_bin_table"

"result scores are the per-generation list of IBD, IBS, numeval,scores and change percents for each objective - for a certain model"
RESULT_SCORES      = "result_"

SUMMARY_RESULTS    = "summary_"

RRS_TABLE = "RRS_TABLE_"
DATA_SUFFIX        = ".datatable"


