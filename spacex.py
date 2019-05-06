import numpy as np
import pandas as pd
from random import shuffle
import copy
from rocket import Rocket
from item import Item

cargo_in_rockets =[]


# read in all the rockets from csv
def ReadRockets(INPUT_CSV):
    rockets = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        rocket = Rocket(row["Spacecraft"], row["Nation"], row['Payload Mass (kgs)'], row['Payload Volume (m3)'],row['Mass (kgs)'], row['Base Cost($)'], row['Fuel-to-Weight'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], [], 0, 0, row['id'])
        rockets.append(rocket)
    return rockets


# read in the cargolist from csv
def ReadCargo(INPUT_CSV):
    cargolist = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        item = Item(row['parcel_ID'], row['mass (kg)'], row['volume (m^3)'], row['mass (kg)']/row['volume (m^3)'])
        cargolist.append(item)
    return cargolist


# function to fill items from cargolist into the rockets by searching for items that match average density in rocket
def fill_cargo(rockets, cargolist):

    filled = 0
    for i in range(3):
        # increase range for search iteratively
        for i in np.arange(0, 1, 0.1):
            items_loaded = []
            for item in cargolist:
                for rocket in rockets:

                    # set upper and lower bound for range of densities
                    rocket_density_upper = (rocket.average_density + rocket.average_density*i)
                    rocket_density_lower = (rocket.average_density - rocket.average_density*i)

                    # if items are within density range and fit the rocket, load in rocket
                    if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                        filled += 1
                        rocket.load_item(item)
                        cargo_in_rockets.append(item)
                        items_loaded.append(item)

            # remove items in cargolist if loaded
            for item in items_loaded:
                cargolist.remove(item)

    # return amount of items filled in current session
    return filled


def fill_cargo_with_error(rockets, cargolist):

    filled = 0
    for i in range(3):
        for rocket in rockets:
            if (rocket.payload_volume - rocket.filled_volume != 0):
                rocket.average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)
            else:
                rocket.average_density = 0
        for i in np.arange(0, 2, 0.1):
        # increase range for search iteratively
            items_loaded = []
            for item in cargolist:
                for rocket in rockets:

                    # calculate shift in density
                    density_difference = rocket.average_density - rocket.initial_average_density

                    # set upper and lower bound for range of densities
                    if density_difference == 0:
                        rocket_density_upper = (rocket.average_density + rocket.average_density*i)
                        rocket_density_lower = (rocket.average_density - rocket.average_density*i)

                    if density_difference > 0:
                        rocket_density_upper = (rocket.average_density + rocket.average_density*i + density_difference*i)
                        rocket_density_lower = (rocket.average_density - rocket.average_density*i + density_difference*i)

                    if density_difference < 0:
                        rocket_density_upper = (rocket.average_density + rocket.average_density*i - density_difference*i)
                        rocket_density_lower = (rocket.average_density - rocket.average_density*i - density_difference*i)

                    # if items are within density range and fit the rocket, load in rocket
                    if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                        filled += 1
                        rocket.load_item_error(item)
                        cargo_in_rockets.append(item)
                        items_loaded.append(item)

            # remove items in cargolist if loaded
            for item in items_loaded:
                cargolist.remove(item)

    # return amount of items filled in current session
    return filled


def fill_cargo_single_rocket(rocket):
    filled = 0

    # increase range for search iteratively
    for i in np.arange(0, 1.5, 0.1):
        items_loaded = []
        for item in cargolist:

            # set upper and lower bound for range of densities
            rocket_density_upper = (rocket.average_density + rocket.average_density*i)
            rocket_density_lower = (rocket.average_density - rocket.average_density*i)

            # if items are within density range and fit the rocket, load in rocket
            if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                rocket.load_item(item)
                cargo_in_rockets.append(item)
                filled += 1
                items_loaded.append(item)

        # remove items in cargolist if loaded
        for item in items_loaded:
            cargolist.remove(item)

    # return amount of items filled in current session
    return filled


def fill_cargo_single_rocket_with_error(rocket):
    filled = 0

    for i in range(3):
        for rocket in rockets:
            if (rocket.payload_volume - rocket.filled_volume != 0):
                rocket.average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)
            else:
                rocket.average_density = 0

    # increase range for search iteratively
        for i in np.arange(0, 1.5, 0.1):
            items_loaded = []
            for item in cargolist:

                # set upper and lower bound for range of densities
                rocket_density_upper = (rocket.average_density + rocket.average_density*i)
                rocket_density_lower = (rocket.average_density - rocket.average_density*i)

                # if items are within density range and fit the rocket, load in rocket
                if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                    rocket.load_item(item)
                    cargo_in_rockets.append(item)
                    filled += 1
                    items_loaded.append(item)

            # remove items in cargolist if loaded
            for item in items_loaded:
                cargolist.remove(item)

    # return amount of items filled in current session
    return filled


# shifts items between rocket in order to make space and try to fit items after each shift.
def switchitems_rockets(rockets):

    # cross check between all rockets
    for rocket_i in rockets:
        for rocket_j in rockets:

            # only for different rockets
            if (rocket_i != rocket_j):

                # cross check for all items in seperate rockets
                for item_i in rocket_i.items:
                    for item_j in rocket_j.items:

                        # if items can switch, do so, and check if item from unfilled list fits in as result
                        if (rocket_j.filled_weight - item_j.mass + item_i.mass <= rocket_j.payload_mass) and (rocket_j.filled_volume - item_j.volume + item_i.volume <= rocket_j.payload_volume) and (rocket_i.filled_weight + item_j.mass - item_i.mass <= rocket_i.payload_mass) and (rocket_i.filled_volume + item_j.volume - item_i.volume <= rocket_i.payload_volume) and (item_i != item_j):

                            # interchange items between the rockets
                            rocket_i.interchange_items(item_i, item_j)
                            rocket_j.interchange_items(item_j, item_i)

                            # try to fit more items
                            filled = fill_cargo(rockets, cargolist)

                            if filled > 0:

                                # break out of rocket.items loops after item is filled
                                break
                                break

                            # switch back items if it did not lead to item filled
                            else:
                                rocket_i.interchange_items(item_j, item_i)
                                rocket_j.interchange_items(item_i, item_j)

def switchitems_rockets_error(rockets):

    # cross check between all rockets
    for rocket_i in rockets:
        for rocket_j in rockets:

            # only for different rockets
            if (rocket_i != rocket_j):

                # cross check for all items in seperate rockets
                for item_i in rocket_i.items:
                    for item_j in rocket_j.items:

                        # if items can switch, do so, and check if item from unfilled list fits in as result
                        if (rocket_j.filled_weight - item_j.mass + item_i.mass <= rocket_j.payload_mass) and (rocket_j.filled_volume - item_j.volume + item_i.volume <= rocket_j.payload_volume) and (rocket_i.filled_weight + item_j.mass - item_i.mass <= rocket_i.payload_mass) and (rocket_i.filled_volume + item_j.volume - item_i.volume <= rocket_i.payload_volume) and (item_i != item_j):

                            # interchange items between the rockets
                            rocket_i.interchange_items(item_i, item_j)
                            rocket_j.interchange_items(item_j, item_i)

                            # try to fit more items
                            filled = fill_cargo_with_error(rockets, cargolist)

                            if filled > 0:

                                # break out of rocket.items loops after item is filled
                                break
                                break

                            # switch back items if it did not lead to item filled
                            else:
                                rocket_i.interchange_items(item_j, item_i)
                                rocket_j.interchange_items(item_i, item_j)


# shifts items between rocket in order to make space and try to fit items after each shift.
# def switchitems_rockets_with_list(rockets):
#
#     # cross check between all rockets
#     for rocket_i in rockets:
#         for rocket_j in rockets:
#
#             # only for different rockets
#             if (rocket_i != rocket_j):
#
#                 rocket_i_items_sub = []
#                 rocket_j_items_sub = []
#
#                 # cross check for all items in seperate rockets
#                 for item_i in rocket_i.items:
#                     for item_j in rocket_j.items:
#
#                         # if items can switch, do so, and check if item from unfilled list fits in as result
#                         if (rocket_j.filled_weight - item_j.mass + item_i.mass <= rocket_j.payload_mass) and (rocket_j.filled_volume - item_j.volume + item_i.volume <= rocket_j.payload_volume) and (rocket_i.filled_weight + item_j.mass - item_i.mass <= rocket_i.payload_mass) and (rocket_i.filled_volume + item_j.volume - item_i.volume <= rocket_i.payload_volume) and (item_i != item_j):
#
#                             # interchange items between the rockets
#                             rocket_i.interchange_items(item_i, item_j)
#                             rocket_j.interchange_items(item_j, item_i)
#
#                             # try to fit more items
#                             filled = fill_cargo(rockets, cargolist)
#
#                             if filled > 0:
#
#                                 # break out of rocket.items loops after item is filled
#                                 break
#                                 break
#
#                             # switch back items if it did not lead to item filled
#                             else:
#                                 rocket_i.interchange_items(item_j, item_i)
#                                 rocket_j.interchange_items(item_i, item_j)


def interchange_item_list(list, item_1, item_2):
    for i in range(len(list)):
        if list[i] == item_1:
            list[i] = item_2


def switchitems_rocket_and_list(rockets):

    for item_list in cargolist:
        for rocket in rockets:
            for item_rocket in rocket.items:

                # check is item in rocket can be swapped with item from cargo_unfilled
                if (rocket.filled_weight - item_rocket.mass + item_list.mass <= rocket.payload_mass) and (rocket.filled_volume - item_rocket.volume + item_list.volume <= rocket.payload_volume) and (item_list != item_rocket):

                    # switch items between rocket and list
                    rocket.interchange_items(item_rocket, item_list)
                    interchange_item_list(cargolist, item_list, item_rocket)

                    # try to fill item
                    filled = fill_cargo_single_rocket(rocket)

                    if (filled) > 0:
                        return 1

                    # if switch did not result in filled item, switch back
                    else:
                        rocket.interchange_items(item_list, item_rocket)
                        interchange_item_list(cargolist, item_rocket, item_list)
    return 0


def switchitems_rocket_and_list_error(rockets):

    for item_list in cargolist:
        for rocket in rockets:
            for item_rocket in rocket.items:

                # check is item in rocket can be swapped with item from cargo_unfilled
                if (rocket.filled_weight - item_rocket.mass + item_list.mass <= rocket.payload_mass) and (rocket.filled_volume - item_rocket.volume + item_list.volume <= rocket.payload_volume) and (item_list != item_rocket):

                    # switch items between rocket and list
                    rocket.interchange_items(item_rocket, item_list)
                    interchange_item_list(cargolist, item_list, item_rocket)

                    # try to fill item
                    filled = fill_cargo_single_rocket_with_error(rocket)

                    if (filled) > 0:
                        return 1

                    # if switch did not result in filled item, switch back
                    else:
                        rocket.interchange_items(item_list, item_rocket)
                        interchange_item_list(cargolist, item_rocket, item_list)
    return 0


def check_items_rocket_cargo(rockets, cargolist):
    yes = 0
    no = 0

    for rocket in rockets:
        for item in rocket.items:
            if item in cargolist:
                yes += 1
            else:
                no += 1
    print(yes)
    print(no)


def check_if_correct(rockets):
        total_filled_mass = 0
        total_filled_volume = 0
        total_volume_items = 0
        total_mass_items = 0
        for rocket in rockets:
            total_filled_mass += rocket.filled_weight
            total_filled_volume += rocket.filled_volume
            for item in rocket.items:
                total_volume_items += item.volume
                total_mass_items += item.mass
        print(total_filled_mass)
        print(total_mass_items)
        print(total_filled_volume)
        print(total_volume_items)


def summary(rockets):
    total_cost = 0
    for rocket in rockets:
        print(rocket.spacecraft)
        print(rocket.payload_mass - rocket.filled_weight)
        print(rocket.payload_volume - rocket.filled_volume)
        Fuel_grams = (rocket.mass + rocket.filled_weight)*(rocket.fuel_to_weight)/(1 - rocket.fuel_to_weight)
        cost_rocket = (rocket.base_cost * (10**6)) + round(1000 * Fuel_grams)
        print(cost_rocket)
        total_cost += cost_rocket
    return total_cost


if __name__ == "__main__":

    # while(len(cargo_in_rockets) < 97):

    rockets = ReadRockets('rockets.csv')
    cargolist = ReadCargo('CargoLists/CargoList1.csv')

    cargo_in_rockets =[]

    # shuffle(cargolist)

    fill_cargo_with_error(rockets, cargolist)
    print(len(set(cargo_in_rockets)))

    switchitems_rockets(rockets)
    print(len(set(cargo_in_rockets)))

    print('----')

    possibility = 1
    while(possibility == 1):
        possibility = switchitems_rocket_and_list(rockets)
        print(len(set(cargo_in_rockets)))
            # print(possibility)

    check_if_correct(rockets)
    total_cost = summary(rockets)
    print(total_cost)
    #
    # for rocket in rockets:
    #     print(rocket.spacecraft)
    #     for item in rocket.items:
    #         print("'" + item.parcel_ID + "'"  + ',')
