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

"""

Random Stuff
------------

"""

import random
from Graphics.charter import charter_reporter, statistic_reporter, comparision_reporter
from Graphics.summary import generate_summary
from jmoo_jmoea import jmoo_evo
from jmoo_properties import DECISION_BIN_TABLE, DATA_SUFFIX, DATA_PREFIX, DEFECT_PREDICT_PREFIX, SUMMARY_RESULTS, \
    RRS_TABLE
from jmoo_stats_box import percentChange

any = random.uniform
normal = random.gauss
seed = random.seed


def readpf(problem):
    filename = "./PF/" + problem.name + "(" + str(len(problem.objectives)) + ")-PF.txt"
    f = open(filename, "r")
    true_PF = []
    for line in f:
        temp = []
        for x in line.split():
            temp.append(float(x))
        true_PF.append(temp)
    return true_PF


def sometimes(p):
    "Returns True at probability 'p;"
    return p > any(0, 1)


def one(lst):
    "Returns one item in a list, selected at random"
    return lst[int(any(0, len(lst) - 1))]


def chosen_one(problem, lst):
    def sum(ll):
        l = ll.fitness.fitness
        # print "l: ", l
        assert len(problem.objectives) == len(l), "Something is wrong here"
        new = []
        for i, o in enumerate(problem.objectives):
            if o.lismore is False:
                new.append(l[i])
            else:
                new.append(100 - l[i])
            return min(new)

    print "Length of frontier: ", len(lst)
    chosen = lst[0]

    for element in lst:
        if sum(chosen) < sum(element):
            chosen = element

    return chosen


"Brief notes"
"Core Part of JMOO accessed by jmoo_interface."

from jmoo_defect_chart import *
from joes_stats_suite import joes_stats_reporter
import time


class jmoo_stats_report:
    def __init__(self, tests, Configurations):
        self.tests = tests
        self.Configurations = Configurations

    def doit(self, tagnote=""):
        joes_stats_reporter(self.tests.problems, self.tests.algorithms, self.Configurations, tag=tagnote)


class jmoo_decision_report:
    def __init__(self, tests):
        self.tests = tests

    def doit(self, tagnote=""):
        joes_decision_reporter(self.tests.problems, self.tests.algorithms, tag=tagnote)


class jmoo_chart_report:
    def __init__(self, tests, Configurations):
        self.tests = tests
        self.Configurations = Configurations

    def doit(self, tagnote=""):
        generate_final_frontier_for_gale4(self.tests.problems, self.tests.algorithms, self.Configurations, tag=tagnote)
        hv_spread =[]
        for problem in self.tests.problems:
            hv_spread.append(charter_reporter([problem], self.tests.algorithms, self.Configurations, tag=tagnote))
        statistic_reporter(self.tests.problems, self.tests.algorithms, self.Configurations, tag=tagnote)
        comparision_reporter(self.tests.problems, self.tests.algorithms, [hvp[0] for hvp in hv_spread], [hvp[1] for hvp in hv_spread], "GALE")
        # for problem in self.tests.problems:
        #     hv_spread.append(charter_reporter([problem], self.tests.algorithms, self.Configurations, tag=tagnote))
        generate_summary(self.tests.problems, self.tests.algorithms, "GALE", self.Configurations)


def generate_final_frontier_for_gale4(problems, algorithms, Configurations, tag=""):
    if "GALE4" not in [algorithm.name for algorithm in algorithms]: return
    else:
        for problem in problems:
            from Graphics.PerformanceMeasures.DataFrame import ProblemFrame
            data = ProblemFrame(problem, [a for a in algorithms if a.name == "GALE4"])

            # data for all repeats
            total_data = [data.get_frontier_values(gen_no) for gen_no in xrange(Configurations["Universal"]["No_of_Generations"])]

            data_for_all_generations = []
            for repeat in xrange(Configurations["Universal"]["Repeats"]):
                temp_data = []
                for gen_no in xrange(Configurations["Universal"]["No_of_Generations"]):
                    temp_data.extend(total_data[gen_no]["GALE4"][repeat])

                from jmoo_individual import jmoo_individual
                solutions = [jmoo_individual(problem, td.decisions, problem.evaluate(td.decisions)) for td in temp_data]

                # non dominated sorting
                from jmoo_algorithms import selNSGA2
                final_solutions, _ = selNSGA2(problem, [], solutions, Configurations)

                for i in xrange(Configurations["Universal"]["No_of_Generations"]):
                    filename = "./RawData/PopulationArchives/" + "GALE4" + "_" + problem.name + "/" + str(repeat) + "/" + \
                               str(i+1) + ".txt"
                    f = open(filename, "w")
                    for fs in final_solutions:
                        f.write(','.join([str(fss) for fss in fs.decisionValues]) + "," + ",".join([str(fss) for fss in fs.fitness.fitness]) + "\n")
                    f.close()




class jmoo_df_report:
    def __init__(self, tag="stats", tests=None):
        self.filename = DEFECT_PREDICT_PREFIX + "DefectPredict.xml"
        self.tag = tag
        self.tests = tests

    def doit(self, tagnote=""):
        if self.tag == "stats":
            self.doStatistics()
        elif self.tag == "Charts":
            self.doCharts()
        elif self.tag == "ranking":
            self.doRanks()

    def doStatistics(self):
        parseXML(self.filename, self.tag)

    def doCharts(self):
        parseXML(self.filename, self.tag)

    def doRanks(self):
        assert (self.tests != None), "Problems not passed"
        parseXML(self.filename, self.tag, self.tests)


class jmoo_test:
    def __init__(self, problems, algorithms):
        self.problems = problems
        self.algorithms = algorithms

    def __str__(self):
        return str(self.problems) + str(self.algorithms)


class JMOO:
    def __init__(self, tests, reports, configurations):
        self.tests = tests
        self.reports = reports
        self.configurations = configurations

    def doTests(self):

        sc2 = open(DATA_PREFIX + SUMMARY_RESULTS + DATA_SUFFIX, 'w')

        # Main control loop
        representatives = []                        # List of resulting final generations (stat boxe datatype)
        record_string = "<Experiment>\n"
        for problem in self.tests.problems:
              
            record_string += "<Problem name = '" + problem.name + "'>\n"
            
            for algorithm in self.tests.algorithms:
                
                
                record_string += "<Algorithm name = '" + algorithm.name + "'>\n"
                
                print "#<------- " + problem.name + " + " + algorithm.name + " ------->#"

                # Initialize Data file for recording summary information [for just this problem + algorithm]
                backend = problem.name + "_" + algorithm.name + ".txt"

                # Decision Data
                filename = problem.name + "-p" + str(self.configurations["Universal"]["Population_Size"]) + "-d" + str(
                    len(problem.decisions)) + "-o" + str(len(problem.objectives)) + "_" + algorithm.name + DATA_SUFFIX
                dbt = open(DATA_PREFIX + DECISION_BIN_TABLE + "_" + filename, 'w')
                sr = open(DATA_PREFIX + SUMMARY_RESULTS + filename, 'w')
                rrs = open(DATA_PREFIX + RRS_TABLE + "_" + filename, 'w')

                # Results Record:
                # # # Every generation
                # # # Decisions + Objectives

                # Summary Record
                # - Best Generation Only
                # - Number of Evaluations + Aggregated Objective Score
                # - 


                fa = open("Data/results_" + filename, 'w')
                strings = ["NumEval"] \
                          + [obj.name + "_median,(%chg),"
                             + obj.name + "_spread" for obj in problem.objectives] \
                          + ["IBD,(%chg), IBS"] + ["IGD,(%chg)"]
                for s in strings: fa.write(s + ",")
                fa.write("\n")
                fa.close()

                IGD_Values = []
                # Repeat Core
                for repeat in range(self.configurations["Universal"]["Repeats"]):

                    foldername = "./RawData/PopulationArchives/" + algorithm.name + "_" + problem.name + "/" + str(repeat)
                    import os
                    if not os.path.exists(foldername):
                        os.makedirs(foldername)
                    # Run
                    record_string += "<Run id = '" + str(repeat+1) + "'>\n"

                    start = time.time()
                    statBox = jmoo_evo(problem, algorithm, self.configurations)
                    end = time.time()

                    # Find best generation
                    representative = statBox.box[0]
                    for r, rep in enumerate(statBox.box):
                        # for indi in rep.population:
                        #     print indi
                        if rep.IBD < representative.IBD:
                            representative = statBox.box[r]
                    representatives.append(representative)

                    # Decision Bin Data
                    s = ""
                    for row in representative.population:
                        for dec in row.decisionValues:
                            s += str("%10.2f" % dec) + ","
                        if row.valid:
                            for obj in row.fitness.fitness:
                                s += str("%10.2f" % obj) + ","
                        else:
                            for obj in problem.objectives:
                                s += "?" + ","

                        s += str(representative.numEval) + ","
                        s += "\n"

                    dbt.write(s)

                    baseline = problem.referencePoint
                    s = ""
                    for row in representative.population:
                        # if not row.valid:
                        #    row.evaluate()
                        if row.valid:
                            for o, base, obj in zip(row.fitness.fitness, baseline, problem.objectives):
                                c = percentChange(o, base, obj.lismore, obj.low, obj.up)
                                s += c + ","
                            s += str(representative.numEval) + ","
                            for o, base, obj in zip(row.fitness.fitness, baseline, problem.objectives):
                                c = str("%12.2f" % o)
                                s += c + ","
                            s += "\n"
                    rrs.write(s)

                    # output every generation
                    for box in [representative]:
                        s_out = ""
                        s_out += str(self.configurations["Universal"]["Population_Size"]) + ","
                        s_out += problem.name + "-p" + str(
                            self.configurations["Universal"]["Population_Size"]) + "-d" + str(
                            len(problem.decisions)) + "-o" + str(len(problem.objectives)) + ","
                        s_out += algorithm.name + ","
                        s_out += str(box.numEval) + ","
                        for low in representative.fitnessMedians:
                            s_out += str("%10.2f" % low) + ","
                        s_out += str("%10.2f" % box.IBD) + "," + str("%10.2f" % box.IBS) + "," + str((end - start))
                        sr.write(s_out + "\n")
                        sc2.write(s_out + "\n")


                    record_string += "<Summary>\n"
                    record_string += "<NumEvals>" + str(representative.numEval) + "</NumEvals>\n"
                    record_string += "<RunTime>" + str((end-start)) + "</RunTime>\n"
                    record_string += "<IBD>" + str(box.IBD) + "</IBD>\n"
                    record_string += "<IBS>" + str(box.IBS) + "</IBS>\n"
                    for i in range(len(problem.objectives)):
                        record_string += "<" + problem.objectives[i].name + ">" + str(representative.fitnessMedians[i]) + "</" + problem.objectives[i].name + ">\n"
                    record_string += "</Summary>"
                        
                        
                    
                    
                    # Finish
                    record_string += "</Run>\n"
                    print " # Finished: Celebrate! # " + " Time taken: " + str("%10.5f" % (end-start)) + " seconds."
                    
                record_string += "</Algorithm>\n"
            record_string += "</Problem>\n"
        record_string += "</Experiment>\n"

        from time import strftime
        date_folder_prefix = strftime("%m-%d-%Y")
        if not os.path.isdir('./RawData/ExperimentalRecords/' + date_folder_prefix):
            os.makedirs('./RawData/ExperimentalRecords/' + date_folder_prefix)
        record_number = len([name for name in os.listdir('./RawData/ExperimentalRecords/' + date_folder_prefix)]) + 1
        filename = './RawData/ExperimentalRecords/' + date_folder_prefix + '/Record' + "_" + str("%02d" % record_number) + "_" + 'ExperimentRecords.xml'
        zOutFile = open(filename, 'w')
        zOutFile.write(record_string)
                    
                    
                    
    def doReports(self,thing=""):
        for report in self.reports:
            report.doit(tagnote=thing)
