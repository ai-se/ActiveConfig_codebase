import os
import sys
import inspect
import random

from jmoo_individual import *
from jmoo_algorithms import *
from jmoo_stats_box import *
import jmoo_properties


def three_others(individuals, one):
    """
    :param individuals: members of the population
    :param one: individual used for mutation
    :return: three other members of the population
    """
    seen = [one]
    def other():
        while True:
            random_selection = random.randint(0, len(individuals) - 1)
            if individuals[random_selection] not in seen:
                seen.append(individuals[random_selection])
                break
        return individuals[random_selection]
    return other(), other(), other()


def trim(mutated, low, up):
    """Constraint checking of decision"""
    return max(low, min(mutated, up))


def crossover(problem, candidate_a, candidate_b):
    """Crossover operator"""
    assert(len(candidate_a) == len(candidate_b)), "Candidate length are not the same"
    crossover_point = random.randrange(1, len(candidate_a), 1)
    assert(crossover_point < len(candidate_a)), "Crossover point has gone overboard"
    mutant = list(candidate_a[:crossover_point])
    mutant.extend(list(candidate_b[crossover_point:]))
    assert(len(mutant) == len(candidate_a)), "Mutant created doesn't have the same length as candidates"
    return mutant


def extrapolate(problem, individuals, one, f, cf):
    from random import randint
    two, three, four = three_others(individuals, one)
    solution = []
    for d, decision in enumerate(problem.decisions):
        assert isinstance(two, jmoo_individual)
        x, y, z = two.decisionValues[d], three.decisionValues[d], four.decisionValues[d]
        if random.random() < cf or randint(0, len(problem.decisions)) == d:
            solution.append(trim(x + f * (y - z), decision.low, decision.up))
        else: solution.append(one.decisionValues[d])

    return jmoo_individual(problem, [float(d) for d in solution], None)


def better(problem,individual,mutant):
    assert(len(individual.fitness.fitness) == len(mutant.fitness.fitness)), "Length of mutant and parent should be the same"
    if len(individual.fitness.fitness) > 1:
        weights = []
        for obj in problem.objectives:
            # w is negative when we are maximizing that objective
            if obj.lismore:  weights.append(+1)
            else:  weights.append(-1)
        weighted_individual = [c*w for c,w in zip(individual.fitness.fitness, weights)]
        weighted_mutant = [c*w for c,w in zip(mutant.fitness.fitness, weights)]
        individual_loss = loss(weighted_individual, weighted_mutant, mins = [obj.low for obj in problem.objectives], maxs = [obj.up for obj in problem.objectives])
        mutant_loss = loss(weighted_mutant, weighted_individual, mins = [obj.low for obj in problem.objectives], maxs = [obj.up for obj in problem.objectives])

        if individual_loss < mutant_loss:  return mutant
        else:  return individual  # otherwise
    else:
        assert(len(individual.fitness.fitness) == len(mutant.fitness.fitness)), "length of the objectives are not equal"
        if problem.objectives[-1].lismore:
            indi = 100 - individual.fitness.fitness[-1]
            mut = 100 - mutant.fitness.fitness[-1]
        else:
            indi = individual.fitness.fitness[-1]
            mut = mutant.fitness.fitness[-1]
        if indi >= mut:  return individual
        else:  return mutant


def de_selector(problem, individuals, configuration, values_to_be_passed):
    newer_generation = []
    no_evals = 0
    for individual in individuals:
        if not individual.valid:
            individual.evaluate()
    no_evals = 0
    for individual in individuals:

        mutant = extrapolate(problem, individuals, individual, configuration["DE"]["F"], configuration["DE"]["CF"])
        mutant.evaluate()
        no_evals += 1
        newer_generation.append(better(problem, individual, mutant))

    # print find_median([pop.fitness.fitness for pop in newer_generation])

    return newer_generation, no_evals


def de_mutate(problem, population, configurations):
    return population, 0


def de_recombine(problem, unusedSlot, mutants, configurations):
    return mutants, 0
