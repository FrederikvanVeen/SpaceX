import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))

from solution import Solution
import algorithms as al
import pandas as pd
import math
import random
from rocket import Rocket
from item import Item
import algorithms as al
import copy
from matplotlib import pyplot as plt
import time
import csv


def barchart_packing(number_of_results):
    results_sim_an_hill_climber_spacex = [0 for i in range(100)]
    results_sim_an_solo_spacex = [0 for i in range(100)]
    results_random_fill = [0 for i in range(100)]
    results_random_fill_hill_climber = [0 for i in range(100)]
    for i in range(number_of_results):
        # create a duplicate for the shuffled solution for each algorithm
        solution_sim_an_hill_climber_spacex = Solution()
        random.shuffle(solution_sim_an_hill_climber_spacex.cargolist)
        solution_sim_an_solo_spacex = copy.deepcopy(solution_sim_an_hill_climber_spacex)
        solution_random_fill = copy.deepcopy(solution_sim_an_hill_climber_spacex)
        solution_random_fill_hill_climber = copy.deepcopy(solution_sim_an_hill_climber_spacex)

        # run all the algorithms on the same shuffled cargolist
        al.sim_an_hill_climber_spacex(solution_sim_an_hill_climber_spacex)
        al.sim_an_solo_spacex(solution_sim_an_solo_spacex)
        al.random_fill(solution_random_fill)
        al.random_fill_hill_climber(solution_random_fill_hill_climber)
        results_sim_an_hill_climber_spacex[solution_sim_an_hill_climber_spacex.items_count] += 1
        results_sim_an_solo_spacex[solution_sim_an_solo_spacex.items_count] += 1
        results_random_fill[solution_random_fill.items_count] += 1
        results_random_fill_hill_climber[solution_random_fill_hill_climber.items_count] +=1
    print(results_sim_an_hill_climber_spacex)
    print(results_random_fill)


def barchart_cost_optimization(number_of_results, cargolist_number, items_packed):
    results_sim_an = []
    results_greedy = []
    results_hill_climber = []
    cargolist_number = str(cargolist_number)
    for i in range(number_of_results):
        items_packed = 0
        while(items_packed < 97):
            solution = Solution(cargolist_number)
            random.shuffle(solution.cargolist)
            al.sim_an_hill_climber_spacex(solution)
            items_packed = solution.items_count
            print(solution.items_count)


def average_running_time_for_packing(cargolist_number, algorithm):
        cargolist_number = str(cargolist_number)
        start = time.time()
        for i in range(10):
            items_packed = 0
            while(items_packed < 97):
                solution = Solution(cargolist_number)
                random.shuffle(solution.cargolist)
                algorithm(solution)
                items_packed = solution.items_count
        end = time.time()
        average_time = (end - start) / 10
        print(average_time)


# function solves the packing problem for a cargolist and algorithm and then writes result in csv
def create_results_packing(algorithm, number_of_results, cargolist_number):
    cargolist_number = str(cargolist_number)
    with open(f'results_packing_algorithms/results{cargolist_number}.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(number_of_results):
            solution = Solution(cargolist_number)
            random.shuffle(solution.cargolist)
            start = time.time()
            algorithm(solution)
            end = time.time()
            running_time = (end - start)
            row = [algorithm.__name__, solution.items_count, running_time]
            writer.writerow(row)
    csvFile.close()

if __name__ == "__main__":
    solution1 = Solution(1)
    al.density_based_hill_climber(solution1)
    print(solution1.items_count)

    average_running_time_for_packing(1, al.density_based_hill_climber)
