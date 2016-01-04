from __future__ import division
def get_data_from_archive(problems, algorithms, Configurations, function):
    from PerformanceMeasures.DataFrame import ProblemFrame
    problem_dict = {}
    for problem in problems:
        data = ProblemFrame(problem, algorithms)
        reference_point = data.get_reference_point(Configurations["Universal"]["No_of_Generations"])
        generation_dict = {}
        for generation in xrange(Configurations["Universal"]["No_of_Generations"]):
            population = data.get_frontier_values(generation)
            evaluations = data.get_evaluation_values(generation)
            algorithm_dict = {}
            for algorithm in algorithms:
                repeat_dict = {}
                for repeat in xrange(Configurations["Universal"]["Repeats"]):
                    candidates = [pop.objectives for pop in population[algorithm.name][repeat]]
                    repeat_dict[str(repeat)] = {}
                    if len(candidates) > 0:
                        repeat_dict[str(repeat)]["HyperVolume"] = function(reference_point, candidates)
                        repeat_dict[str(repeat)]["Evaluations"] = evaluations[algorithm.name][repeat]
                    else:
                        repeat_dict[str(repeat)]["HyperVolume"] = None
                        repeat_dict[str(repeat)]["Evaluations"] = None

                algorithm_dict[algorithm.name] = repeat_dict
            generation_dict[str(generation)] = algorithm_dict
        problem_dict[problem.name] = generation_dict
    return problem_dict


def generate_summary(problems, algorithms, baseline, Configurations, tag="Comparisions"):
    for problem in problems:
        print problem.name , " - " * 50
        from PerformanceMeasures.DataFrame import ProblemFrame
        data = ProblemFrame(problem, algorithms)
        population = data.get_frontier_values()

        fast_algorithm_population = []
        for repeat in xrange(Configurations["Universal"]["Repeats"]):
            fast_algorithm_population.append([pop.objectives for pop in population[baseline][repeat]])



        for algorithm in algorithms:
            if algorithm.name != baseline:
                baseline_population = []
                print algorithm.name + " | ",
                for repeat in xrange(Configurations["Universal"]["Repeats"]):
                    baseline_population.append([pop.objectives for pop in population[algorithm.name][repeat]])
                for objective_number in xrange(len(problem.objectives)):
                    fast_algorithm_objective_list = [flat[objective_number] for fap in fast_algorithm_population for flat in fap]
                    baseline_objective_list = [flat[objective_number]  for bp in baseline_population for flat in bp]

                    from numpy import std, mean
                    s = std(baseline_objective_list)
                    small_effect = s * 0.4
                    n1 = mean(baseline_objective_list)
                    n2 = mean(fast_algorithm_objective_list)
                    if abs(n1 - n2) <= small_effect: print "Yes", round(abs(n1 - n2)/(s+0.000000001), 3),
                    else: print "No", round(abs(n1 - n2)/(s+0.000000001), 3),
                    print "|",
                print






