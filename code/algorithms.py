import helpers as hp


# algorithms for filling
def density_based_hill_climber_error(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets

    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_density_with_error)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_single_rocket_density_with_error)

    solution.items_count = len(cargo_in_rockets)


def density_based_hill_climber(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets

    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)
    hp.switchitems_rockets_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_density)

    possibility = 1
    while(possibility == 1):
        possibility = hp.switchitems_rocket_and_list_fill(rockets, cargolist, cargo_in_rockets, hp.fill_cargo_single_rocket_density)

    solution.items_count = len(cargo_in_rockets)


def density_based(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_density_with_error(rockets, cargolist, cargo_in_rockets)
    solution.items_count = len(cargo_in_rockets)


def random_fill(solution):
    rockets = solution.rockets
    cargolist = solution.cargolist
    cargo_in_rockets = solution.cargo_in_rockets
    hp.fill_cargo_random(rockets, cargolist, cargo_in_rockets)
    solution.items_count = len(cargo_in_rockets)


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


def packing_cargolist_3(solution):
    cargolist = solution.cargolist
    rockets = solution.rockets
    cargo_in_rockets = solution.cargo_in_rockets


#  algorithms for cost optimisation
def sim_an_cost(solution, T_begin, iter_no):
    T = T_begin
    rockets = solution.rockets
    for i in range(iter_no):
        hp.cost_opitimization_probability_depended(rockets, T)
        T = hp.update_temperature(T)


def hill_climber_cost(solution):
    rockets = solution.rockets
    cost_before = hp.cost
    hp.cost_opitimization_hill_climber(rockets)
    total_cost = hp.cost(rockets)


def greedy_cost(solution):
    rockets = solution.rockets
    hp.cost_opitimization_greedy(rockets)
