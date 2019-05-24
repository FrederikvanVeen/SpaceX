import helpers as hp


# algorithm for filling by density with hill climber
def density_based_hill_climber_error(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets

    # fill rockets based on density
    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)

    # switch items between rockets and remaining items in cargolist
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_density_with_error)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_single_rocket_density_with_error)

    solution.items_count = len(cargo_in_rockets)


# algorithm for filling by density with hill climber without error correct
def density_based_hill_climber(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets

    # fill rockets based on density with error
    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)

    # switch items between rockets and remaining items in cargolist
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_density)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_single_rocket_density)

    solution.items_count = len(cargo_in_rockets)


# algorithm to fill rockets based on density
def density_based(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)
    solution.items_count = len(cargo_in_rockets)


# algorithm that fills rockets random
def random_fill(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_random(rockets, cargolist, cargo_in_rockets)
    solution.items_count = len(cargo_in_rockets)


# algorithm fills rockets random and switches parcel in order to create a more efficient configuration
def random_fill_hill_climber(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_random(rockets, cargolist, cargo_in_rockets)
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_random)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_single_rocket_random)

    solution.items_count = len(cargo_in_rockets)


#  algorithm simulated annealing in order to optimize cost
def sim_an_cost(solution, T_begin, iter_no):
    T = T_begin
    rockets = solution.rockets
    for i in range(iter_no):
        hp.cost_opitimization_probability_depended(rockets, T)
        T = hp.update_temperature(T)


# hill climber for cost optimization
def hill_climber_cost(solution):
    rockets = solution.rockets
    cost_before = hp.cost
    hp.cost_opitimization_hill_climber(rockets)
    total_cost = hp.cost(rockets)


# greedy for cost optimization
def greedy_cost(solution):
    rockets = solution.rockets
    hp.cost_opitimization_greedy(rockets)
