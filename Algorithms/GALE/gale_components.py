"""
    This file is part of GALE,
    Copyright Joe Krall, 2014.

    GALE is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    GALE is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with GALE.  If not, see <http://www.gnu.org/licenses/>.
"""

from Fastmap.Slurp import *
from Fastmap.Moo import *
from jmoo_individual import *


def galeWHERE(problem, population, configuration, values_to_be_passed):
    "The Core method behind GALE"

    # Compile population into table form used by WHERE
    t = slurp([[x for x in row.decisionValues] + ["?" for y in problem.objectives] for row in population],
              problem.buildHeader().split(","))

    # Initialize some parameters for WHERE
    The.allowDomination = True
    The.alpha = 1
    for i, row in enumerate(t.rows):
        row.evaluated = False

    # Run WHERE
    m = Moo(problem, t, len(t.rows), N=1).divide(minnie=rstop(t))

    # Organizing
    NDLeafs = m.nonPrunedLeaves()  # The surviving non-dominated leafs
    allLeafs = m.nonPrunedLeaves() + m.prunedLeaves()  # All of the leafs

    # After mutation: Check how many rows were actually evaluated
    numEval = 0
    for leaf in allLeafs:
        for row in leaf.table.rows:
            if row.evaluated:
                numEval += 1

    return NDLeafs, numEval




def galeMutate(problem, NDLeafs, configuration):
    #################
    # Mutation Phase
    #################
# Keep track of evals
    numEval = 0

    for leaf in NDLeafs:

        # print "Number of mutants: ", len(leaf.table.rows)
        # Pull out the Poles
        east = leaf.table.rows[0]
        west = leaf.table.rows[-1]

        # Evaluate those poles if needed
        if not east.evaluated:
            for o, objScore in enumerate(problem.evaluate(east.cells)):
                east.cells[-(len(problem.objectives) - o)] = objScore
            east.evaluated = True
            numEval += 1
        if not west.evaluated:
            for o, objScore in enumerate(problem.evaluate(west.cells)):
                west.cells[-(len(problem.objectives) - o)] = objScore
            west.evaluated = True
            numEval += 1

        # Score the poles
        n = len(problem.decisions)
        weights = []
        for obj in problem.objectives:
            # w is negative when we are maximizing that objective
            if obj.lismore:
                weights.append(+1)
            else:
                weights.append(-1)
        weightedWest = [c * w for c, w in zip(west.cells[n:], weights)]
        weightedEast = [c * w for c, w in zip(east.cells[n:], weights)]
        westLoss = loss(weightedWest, weightedEast, mins=[obj.low for obj in problem.objectives],
                        maxs=[obj.up for obj in problem.objectives])
        eastLoss = loss(weightedEast, weightedWest, mins=[obj.low for obj in problem.objectives],
                        maxs=[obj.up for obj in problem.objectives])

        # Determine better Pole
        if eastLoss < westLoss:
            SouthPole, NorthPole = east, west
        else:
            SouthPole, NorthPole = west, east

        # Magnitude of the mutations
        g = abs(SouthPole.x - NorthPole.x)

        # Iterate over the individuals of the leaf
        for row in leaf.table.rows:

            # Make a copy of the row in case we reject it
            copy = [item for item in row.cells]
            cx = row.x

            for attr in range(0, len(problem.decisions)):

                # just some naming shortcuts
                me = row.cells[attr]
                good = SouthPole.cells[attr]
                bad = NorthPole.cells[attr]
                dec = problem.decisions[attr]

                # Find direction to mutate (Want to mutate towards good pole)
                if me > good:  d = -1
                if me < good:  d = +1
                if me == good: d = 0

                row.cells[attr] = min(dec.up, max(dec.low, (me + me * g * d) * configuration["GALE"]["DELTA"]))

            # Project the Mutant
            a = row.distance(NorthPole)
            b = row.distance(SouthPole)
            c = NorthPole.distance(SouthPole)
            x = (a ** 2 + row.c ** 2 - b ** 2) / (2 * row.c + 0.00001)

            # Test Mutant for Acceptance
            # confGAMMA = 0.15 #note: make this a property

            # print abs(cx-x), (cx + (g * configuration["GALE"]["GAMMA"]))
            if abs(x - cx) > (g * configuration["GALE"]["GAMMA"]) or problem.evalConstraints(
                    row.cells[:n]):  # reject it
                row.cells = copy
                row.x = x


    # After mutation; Convert back to JMOO Data Structures
    population = []
    for leaf in NDLeafs:
        for row in leaf.table.rows:
            if row.evaluated:
                population.append(jmoo_individual(problem, [x for x in row.cells[:len(problem.decisions)]],
                                                  [x for x in row.cells[len(problem.decisions):]]))
            else:
                population.append(jmoo_individual(problem, [x for x in row.cells[:len(problem.decisions)]], None))

                # Return selectees and number of evaluations
    return population, numEval


def galeRegen(problem, unusedslot, mutants, configuration):
    howMany = configuration["Universal"]["Population_Size"] - len(mutants)
    # Generate random individuals
    population = []
    for i in range(howMany):
        population.append(jmoo_individual(problem, problem.generateInput(), None))
    
    return mutants+population, 0
