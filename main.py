import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))

from solution import Solution
import algorithms as al
import random
import copy
from matplotlib import pyplot as plt
import time
import csv
from helpers import maxitems


def barchart_packing(number_of_results, cargolist_number):
    results_sim_an_hill_climber_spacex = [0 for i in range(100)]
    results_sim_an_solo_spacex = [0 for i in range(100)]
    results_random_fill = [0 for i in range(100)]
    results_random_fill_hill_climber = [0 for i in range(100)]
    for i in range(number_of_results):
        # create a duplicate for the shuffled solution for each algorithm
        solution_sim_an_hill_climber_spacex = Solution(cargolist_number)
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


def barchart_cost_optimization(number_of_results, cargolist_number):
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


# calculates average running time for packing algorithms
def average_running_time_for_packing(cargolist_number, algorithm, goal_items_packed):
        cargolist_number = str(cargolist_number)
        start = time.time()
        for i in range(10):
            items_packed = 0
            while(items_packed < goal_items_packed):
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


# not finished yet
def create_results_cost_optimization(number_of_results, cargolist_number, goal_items_packed):
    cargolist_number = str(cargolist_number)
    with open(f'results_cost_optimization_algorithms/algorithmsperformances/resultscargolist{cargolist_number}.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        for i in range(number_of_results):
            items_packed = 0

            # get starting configuration for required amount of items
            while(items_packed < goal_items_packed):
                solution1 = Solution(cargolist_number)
                random.shuffle(solution1.cargolist)
                al.density_based_hill_climber_error(solution1)
                items_packed = solution1.items_count
            print(i)
            # calculate cost of configuration
            solution1.calculate_cost()

            # create equivalent copies of the solution
            solution2 = copy.deepcopy(solution1)
            solution3 = copy.deepcopy(solution1)

            # optimize cost for equivalent solutions using sim an and write score in csv
            start = time.time()
            al.sim_an_cost(solution1, 200, 50)
            end = time.time()
            running_time = (end - start)
            solution1.calculate_cost()
            row = ['simulated annealing', solution1.cost, running_time]
            writer.writerow(row)

            # optimize cost for equivalent solutions using hill climber and write score in csv
            start = time.time()
            al.hill_climber_cost(solution2)
            end = time.time()
            running_time = (end - start)
            solution2.calculate_cost()
            row = ['hill climber', solution2.cost, running_time]
            writer.writerow(row)

            # optimize cost for equivalent solutions using greedy and write score in csv
            start = time.time()
            al.greedy_cost(solution3)
            end = time.time()
            running_time = (end - start)
            solution3.calculate_cost()
            row = ['greedy', solution3.cost, running_time]
            writer.writerow(row)

    csvFile.close()

# function to determine
def best_cost_optimization_algorithm(number_of_results, cargolist_number):
        cargolist_number = str(cargolist_number)
        with open(f'results_cost_optimization_algorithms/best_performing_algorithm/resultscargolist{cargolist_number}test.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)

            for i in range(number_of_results):

                # create solution and pack rockets
                solution1 = Solution(cargolist_number)
                random.shuffle(solution1.cargolist)
                al.density_based_hill_climber(solution1)
                solution1.calculate_cost()

                # create equivalent copies of the solution
                solution2 = copy.deepcopy(solution1)
                solution3 = copy.deepcopy(solution1)


                # optimize cost for equivalent solutions using the different algorithms
                al.sim_an_cost(solution1, 200, 50)
                al.hill_climber_cost(solution2)
                al.greedy_cost(solution3)

                # calculate costs after optimization
                solution1.calculate_cost()
                solution2.calculate_cost()
                solution3.calculate_cost()
                print(solution1.cost)
                print(solution2.cost)
                print(solution3.cost)

                # determine beste performing algorithm
                if solution1.cost <= solution2.cost:
                    if solution1.cost < solution3.cost:
                        best  = 'simulated annealing'
                    if solution1.cost > solution3.cost:
                        best  = 'greedy'
                    if solution1.cost > solution3.cost:
                        best = 'simulated annealing and greedy'
                else:
                    if solution2.cost < solution3.cost:
                        best  = 'hill climber'
                    if solution2.cost > solution3.cost:
                        best  = 'greedy'
                    if solution2.cost == solution3.cost:
                        best = 'greedy and hill climber'

                # write best performing algorithm in csv
                row = [i + 1, best]
                writer.writerow(row)
        # close csv
        csvFile.close()

def packing_cargolist_3():
    solution = Solution(3)
    solution.rockets = solution.ReadRockets("data/rocketssix.csv")


 # For d) and e): use cargolist to fill all rockets, without removing items from cargolist, then check which rocket has best cost per item and choose that one
 # sort of greedy(density_based_hill_climber)

if __name__ == "__main__":
    solution = Solution(2)
    maxitems(solution.cargolist, solution.rockets)
    solution.cargolist.sort(key=lambda x: x.mass)
    mass_90 = 0
    volume_90 = 0
    for i in range (90):
        mass_90 += solution.cargolist[i].mass
        volume_90 += solution.cargolist[i].volume

    total_mass_rockets = 0
    total_volume_rockets = 0
    for rocket in solution.rockets:
        total_mass_rockets += rocket.payload_mass
        total_volume_rockets += rocket.payload_volume

    print(mass_90/total_mass_rockets)
    print(volume_90/total_volume_rockets)
