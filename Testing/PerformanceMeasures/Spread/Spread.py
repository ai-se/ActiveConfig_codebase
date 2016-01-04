from __future__ import division
def spread_calculator(obtained_front, extreme_point1, extreme_point2):
    """Given a Pareto front `first_front` and the two extreme points of the
    optimal Pareto front, this function returns a metric of the diversity
    of the front as explained in the original NSGA-II article by K. Deb.
    The smaller the value is, the better the front is.
    """

    def euclidean_distance(list1, list2):
        assert(len(list1) == len(list2)), "The points don't have the same dimension"
        distance = sum([(i - j) ** 2 for i, j in zip(list1, list2)]) ** 0.5
        assert(distance >= 0), "Distance can't be less than 0"
        return distance

    def closest(obtained_front, point, distance=euclidean_distance):
        """Returns the point from obtained_front which is closed to point"""
        from sys import maxint
        closest_point = None
        min_distance = maxint
        for opoint in obtained_front:
            temp_distance = distance(opoint, point)
            if temp_distance < min_distance:
                min_distance = temp_distance
                closest_point = opoint
        assert(closest_point is not None), "closest_point cannot be None"
        return closest_point, min_distance

    _, df = closest(obtained_front, extreme_point1)
    _, dl = closest(obtained_front, extreme_point2)

    distances = [euclidean_distance(obtained_front[i], obtained_front[i+1]) for i in xrange(len(obtained_front) -1)]
    distances_mean = sum(distances)/len(distances)
    d_variance = sum([abs(di - distances_mean) for di in distances])
    N = len(obtained_front)

    return (df + dl + d_variance)/(df + dl + (N -1) * distances_mean)


def file_reader(filepath, separator=" "):
    from os.path import isfile
    assert(isfile(filepath) == True), "file doesn't exist"
    content = []
    for line in open(filepath, "r"):
        content.append([float(element) for element in line.split(separator) if element != "\n"])
    return content


def sort_list_of_list(list_of_list):
    """ This function is to extract the extreme points"""
    def sorting_def(list):
        number_of_objectives = len(list)
        weights = reversed([10 ** i for i in xrange(number_of_objectives)])
        return sum([element * weight for element, weight in zip(list, weights)])
    return sorted(list_of_list, key=sorting_def)


def spread_calculator_wrapper():
    true_pf_folder = "./True_PF/"
    obtained_pf_folder = "./Obtained_PF/"

    from os import listdir
    true_pf_files = [true_pf_folder + name for name in listdir(true_pf_folder)]
    obtained_pf_files = [obtained_pf_folder + name for name in listdir(obtained_pf_folder)]

    assert(len(true_pf_files) == len(obtained_pf_files)), "Number of files in both folders should be equal"

    for true_pf_file, obtained_pf_file in zip(true_pf_files, obtained_pf_files):
        true_pf_content = file_reader(true_pf_file)
        obtained_pf_content = file_reader(obtained_pf_file)

        sorted_true_pf_content = sort_list_of_list(true_pf_content)
        sorted_obtained_pf_content = sort_list_of_list(obtained_pf_content)

        first_extreme_solution = sorted_true_pf_content[0]
        second_extreme_solution = sorted_true_pf_content[-1]

        spread = spread_calculator(sorted_obtained_pf_content, first_extreme_solution, second_extreme_solution)
        print "Name: ", true_pf_file, " Spread: ", round(spread, 3)

    return None


spread_calculator_wrapper()
