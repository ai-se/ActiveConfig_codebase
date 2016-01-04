class ProblemFrame():
    def __init__(self, problem, algorithms):
        self.problem = problem
        self.algorithms = algorithms
        self.data = []
        self.get_data()

    def get_data(self):
        self.data = [AlgorithmFrame(self.problem, algorithm) for algorithm in self.algorithms]

    def get_final_frontiers(self, number=-1):
        """
        :param number: Front Number
        :return: List of all the solutions across all algorithms and repeats
        """
        assert (len(self.data) != 0), "The frame was not initialized properly"
        return [item for d in self.data for item in d.get_frontiers_collection(number)]

    def get_extreme_points(self, number_of_generations):
        """This method should be used to find the extreme points of particular generation across all the algorithms"""
        from Techniques.flatten_list import flatten
        points = flatten([d.get_frontiers_collection(number_of_generations) for d in self.data])
        objectives = [point.objectives for point in points]
        maps_objectives = [[-1 for _ in objectives] for _ in objectives]
        from Techniques.euclidean_distance import euclidean_distance
        for i, ii in enumerate(objectives):
            for j, jj in enumerate(objectives):
                if maps_objectives[i][j] == -1:
                    maps_objectives[i][j] = euclidean_distance(ii, jj)
                    maps_objectives[j][i] = euclidean_distance(ii, jj)
                elif i == j:
                    maps_objectives[i][j] = 0
        max_distance = max([max(maps_objective) for maps_objective in maps_objectives])
        indexes = [[(i, j) for j, distance in enumerate(distances) if distance == max_distance] for i, distances in
                   enumerate(maps_objectives)]
        index = [index for index in indexes if len(index) > 0][-1][-1]  # Hack: To handle list of lists
        # indexes should always be a multiple of 2. And if there more than 2 entries in indexes just use any one.

        return objectives[index[0]], objectives[index[1]]

    def get_reference_point(self, number_of_generations):
        """This method should be used to find the reference point or the nadir point"""
        reference_point = [-1 for _ in self.problem.objectives]
        from Techniques.flatten_list import flatten
        points = flatten(
            [d.get_frontiers_collection(number) for number in xrange(number_of_generations) for d in self.data])

        objectives = [point.objectives for point in points]
        for count, objective in enumerate(self.problem.objectives):
            one_objective = [point[count] for point in objectives]
            if objective.lismore is True:
                reference_point[count] = max(one_objective)
            else:
                reference_point[count] = min(one_objective)
        return reference_point

    def get_frontier_values(self, generation_number=-1):
        result = {}
        for d in self.data: result[d.algorithm.name] = d.get_frontiers_for_generation(generation_number)
        return result

    def get_evaluation_values(self, generation_number):
        result = {}
        for d in self.data: result[d.algorithm.name] = d.get_evaluations_for_generation(generation_number)
        return result


class AlgorithmFrame():
    def __init__(self, problem, algorithm):
        self.problem = problem
        self.algorithm = algorithm
        self.foldername = "./RawData/PopulationArchives/" + algorithm.name + "_" + problem.name + "/"
        self.repeats = None
        self.get_repeat_data()

    def get_repeat_data(self):
        import os
        subdirs = [self.foldername + d for d in os.listdir(self.foldername) if os.path.isdir(self.foldername + d)]
        self.repeats = [RepeatFrame(self.problem, subdir) for subdir in subdirs]

    def get_frontiers_collection(self, number):
        return [item for repeat in self.repeats for item in repeat.get_frontier(number)]

    def get_frontiers_for_generation(self, number=-1):
        return [repeat.get_frontier(number) for repeat in self.repeats]

    def get_evaluations_for_generation(self, number):
        return [repeat.get_evaluations(number) for repeat in self.repeats]


class RepeatFrame():
    def __init__(self, problem, folder_name):
        self.problem = problem
        self.foldername = folder_name
        self.generations = []
        self.get_generation_data()

    def get_generation_data(self):
        from os import listdir
        from os.path import isfile, join, getmtime
        files = sorted([join(self.foldername, f) for f in listdir(self.foldername) if isfile(join(self.foldername, f))], key=lambda x: getmtime(x))
        self.generations = [GenerationFrame(self.problem, file) for file in files]

    def get_frontier(self, number):
        if number < len(self.generations):
            return self.generations[number].solutions
        else:
            return []

    def get_evaluations(self, number):
        if number < len(self.generations):
            return self.generations[number].evaluation
        else:
            return 0


class GenerationFrame():
    def __init__(self, problem, filename):
        self.generation_number = filename.split("/")[-1]
        self.filename = filename
        self.problem = problem
        self.solutions = []
        self.evaluation = -1
        self.get_data()

    def get_data(self):
        number_of_decisions = len(self.problem.decisions)
        for line in open(self.filename).readlines():
            content = [float(l) for l in line.replace("\n", "").split(",") if l != "X"]
            self.solutions.append(SolutionFrame(content[:number_of_decisions], content[number_of_decisions:]))
        from Techniques.file_operations import count_number_of_lines
        self.evaluation = count_number_of_lines(self.filename)


class SolutionFrame():
    def __init__(self, decisions, objectives):
        self.decisions = decisions
        self.objectives = objectives

    def __repr__(self):
        return "|".join(map(str, self.decisions + self.objectives))
