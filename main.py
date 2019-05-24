import os, sys
directory = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(directory, "code"))
sys.path.append(os.path.join(directory, "code", "classes"))

from solution import Solution
import algorithms as al
import random
import copy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import time
import csv
from helpers import maxitems

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

        return(average_time)


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

                # determine best performing algorithm
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

def run_programme():
    # welcome the user
    print("A warm welcome to the Space Freight's case from the group 'SpaceX'. You'll have to make a decision which algorithm you'ld like to run in order to fill the rockets with cargo.\n")
    print("First of all, you'll have to decide which cargolist you'ld like to fill the rockets with.\n")
    print("There are three cargolists: \n"
    "Cargolist 1\n"
    "Cargolist 2\n"
    "Cargolist 3\n")
    print("Please choose an option by typing either one of the following numbers: 1, 2 or 3\n")
    option = input("Option: ")
    number = 0
    if option.isdigit():
        if option == "1":
            number = 1
        elif option == "2":
            number = 2
        elif option == "3":
            number = 3
        else:
            print("Invalid command (command must be either an 1, 2 or 3). Please try again.\n")
    else:
        print("Invalid command (command must be an integer). Please try again.\n")
    print("Alright. Now you've decided which cargolist to send to space, it's time to decide which algorithm is going to devide the packages amongst the rockets.\n")
    print("There are four options to choose from:\n"
    "Option one is a random filler\n"
    "Option two is a random filler combined with a hill climber\n"
    "Option three is density based\n"
    "Option four is density based combined with a hill climber\n")
    # request for an algorithm
    print("Please choose an option by typing either one of the following numbers: 1, 2, 3 or 4\n")
    command = input("Option: ")
    solution_chosen_option = []
    if command.isdigit():
        if command == "1":
            solution1 = Solution(number)
            al.random_fill(solution1)
            print(f"The algorithm packed {solution1.items_count} items")
            print(f"The average running time was {average_running_time_for_packing(number, al.random_fill, 75)} seconds")
            solution_chosen_option.append(solution1)
        elif command == "2":
            solution2 = Solution(number)
            al.random_fill_hill_climber(solution2)
            print(f"The algorithm packed {solution2.items_count} items")
            print(f"The average running time was {average_running_time_for_packing(number, al.random_fill_hill_climber, 93)} seconds")
            solution_chosen_option.append(solution2)
        elif command == "3":
            solution3 = Solution(number)
            al.density_based(solution3)
            print(f"The algorithm packed {solution3.items_count} items")
            print(f"The average running time was {average_running_time_for_packing(number, al.density_based, 93)} seconds")
            solution_chosen_option.append(solution3)
        elif command == "4":
            solution4 = Solution(number)
            al.density_based_hill_climber(solution4)
            print(f"The algorithm packed {solution4.items_count} items")
            print(f"The average running time was {average_running_time_for_packing(number, al.density_based_hill_climber, 97)} seconds")
            # solution.append(al.density_based_hill_climber(solution4))
            solution_chosen_option.append(solution4)
            # results_packing = create_results_packing(command, solution4.items_count, number)
        else:
            print("Invalid command (command must be either an 1, 2, 3, or 4). Please try again.\n")
    else:
        print("Invalid command (command must be an integer). Please try again.\n")

    for object in solution_chosen_option:
        solution_first = object
    solution_first.calculate_cost()
    initial_costs = solution_first.cost
    print(f"The total costs are {initial_costs} dollars")

    # inform user about the options
    print("\nAlright. Now you've filled the rockets with cargo, let's run another algorithm in order to reduce the costs as much as possible.\n"
    "Once again, there are several algorithms so you've got to make another decision:\n"
    "Option one is simulated annealing\n"
    "Option two is hill climber\n"
    "Option three is greedy\n")
    # make request for an algorithm
    print("Please make a decision by typing either one of the following numbers: 1, 2 or 3\n")
    # new object
    sol_chosen = []
    # run chosen algorithm
    command = input("Option: ")
    if command.isdigit():
        if command == "1":
            print("Please initialize a beginning temperature and the number of iterations by inserting only integers\n")
            T_begin = int(input("Temperature: "))
            iter_no = int(input("Iterations: "))
            # iter_no = int(iter_no[10:len(iter_no)])
            al.sim_an_cost(solution_first, T_begin, iter_no)
        elif command == "2":
            al.hill_climber_cost(solution_first)
        elif command == "3":
            al.greedy_cost(solution_first)
        else:
            print("Invalid command (command must be either an 1, 2 or 3). Please try again.\n")
    else:
        print("Invalid command (command must be an integer). Please try again.\n")

    solution_first.calculate_cost()
    final_costs = solution_first.cost
    saved = initial_costs - final_costs
    print(f"The total costs are now {final_costs} dollars.\n"
    f"The algorithm reduced the costs with {saved} dollars!\n")


if __name__ == "__main__":
    run_programme()

    # generate best algorithm to optimize costs
    # best_cost_optimization_algorithm(100, 1)

    # generate results for cost
    # create_results_cost_optimization(100, 1, 97)

    # generate results for packing algorithms
    # create_results_packing(density_based_hill_climber, 100, 1)

    # generate results for running time of packing algorithms
    # average_running_time_for_packing(1, density_based_hill_climber, 97)
