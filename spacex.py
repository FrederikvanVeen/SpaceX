import numpy as np
import pandas as pd
from random import shuffle


cargo_in_rockets =[]
class Rocket():
    def __init__(self, spacecraft, nation, payload_mass, payload_volume, mass, base_cost, fuel_to_weight, average_density, items, filled_weight, filled_volume):
        """
        Initialize a Rocket
        """
        self.spacecraft = spacecraft
        self.nation = nation
        self.payload_mass = payload_mass
        self.payload_volume = payload_volume
        self.mass = mass
        self.base_cost = base_cost
        self.fuel_to_weight = fuel_to_weight
        self.average_density = average_density
        self.items = items
        self.filled_weight = filled_weight
        self.filled_volume = filled_volume

    def __str__(self):
        return str(self.average_density)

class Item():
    def __init__(self, parcel_ID, mass, volume, density):
        """
        Initialize an Item
        """
        self.parcel_ID = parcel_ID
        self.mass = mass
        self.volume = volume
        self.density =density

    def __str__(self):
        return self.parcel_ID

# read in all the rockets from csv
def ReadRockets(INPUT_CSV):
    rockets = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        rocket = Rocket(row["Spacecraft"], row["Nation"], row['Payload Mass (kgs)'], row['Payload Volume (m3)'],row['Mass (kgs)'], row['Base Cost($)'], row['Fuel-to-Weight'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], [], 0, 0)
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


def fill_cargo(rockets, cargolist):
    filled = 0
    for i in range(3):
        for i in np.arange(0, 1, 0.1):
            for item in cargolist:
                for rocket in rockets:
                    rocket_density_upper = (rocket.average_density + rocket.average_density*i)
                    rocket_density_lower = (rocket.average_density - rocket.average_density*i)
                    if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in cargo_in_rockets):
                        load_item_in_rocket(item, rocket)
                        filled += 1
                        cargo_in_rockets.append(item)

    if filled > 0:
        return True
    else:
        return False


# no result
# def fitlastitems(rockets, cargolist):
#     for item in cargolist:
#         for rocket in rockets:
#             if (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in filled_items):
#                 load_item_in_rocket(item, rocket)
#                 filled_items.append(item)


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
                            interchange_items_between_rockets(rocket_i, rocket_j, item_i, item_j)

                            filled = fill_cargo(rockets, cargo_unfilled)
                            #
                            if filled:
                                print('yaa')
                                break
                            #
                            # if not filled:
                            #     interchange_items_between_rockets(rocket_i, rocket_j, item_j, item_i)


def interchange_items_between_rockets(rocket_i, rocket_j, item_i, item_j):
    item_i_temp = item_i
    item_j_temp = item_j

    # update filled weight and volume
    rocket_i.filled_weight = rocket_i.filled_weight + item_j.mass - item_i.mass
    rocket_i.filled_volume = rocket_i.filled_volume + item_j.volume - item_i.volume

    rocket_j.filled_weight = rocket_j.filled_weight + item_i.mass - item_j.mass
    rocket_j.filled_volume = rocket_j.filled_volume + item_i.volume - item_j.volume


    for item in rocket_i.items:
        if item == item_i:
            item = item_j_temp

    for item in rocket_j.items:
        if item == item_j:
            item = item_i_temp



    # for n in range(len(rocket_i.items)):
    #     if rocket_i.items[n] == item_i:
    #         item_temp_temp1 = rocket_i.items[n]
    #         rocket_i.items[n] = item_j_temp
    #
    # for m in range(len(rocket_j.items)):
    #     if rocket_j.items[m] == item_j:
    #         rocket_j.items[m] = item_temp_temp1
    #
    #




#
# def switchitems_rocket_and_unfilled(rockets, cargo_unfilled):
#
#     for rocket in rockets:
#         for item_rocket in rocket.items:
#             for item_list in cargo_unfilled:
#
#                 # check is item in rocket can be swapped with item from cargo_unfilled
#                 if (rocket.filled_weight - item_rocket.mass + item_list.mass <= rocket.payload_mass) and (rocket.filled_volume - item_rocket.volume + item_list.volume <= rocket.payload_volume):
#                     interchange_items_between_rocket_and_list(rocket, cargo_unfilled, item_rocket, item_list)
#                     filled = fill_cargo(rockets, cargo_unfilled)
#                     # if not filled:
#                         # interchange_items_between_rocket_and_list(rocket, cargo_unfilled, item_list, item_rocket)
#
#
# def interchange_items_between_rocket_and_list(rocket, cargo_unfilled, item_rocket, item_list):
#     # update filled weight and volume
#
#     rocket.filled_weight = rocket.filled_weight + item_list.mass - item_rocket.mass
#     rocket.filled_volume = rocket.filled_volume + item_list.volume - item_rocket.volume
#
#     # update rocket
#     for n in range(len(rocket.items)):
#         if (rocket.items[n] == item_rocket):
#             rocket.items[n] = item_list
#
#
#     for n in range(len(cargo_in_rockets)):
#         if cargo_in_rockets[n] == item_rocket:
#             cargo_in_rockets[n] = item_list
#
#     for n in range(len(cargo_unfilled)):
#         if cargo_unfilled[n] == item_list:
#             cargo_unfilled[n] = item_rocket
#

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

def load_item_in_rocket(item, rocket):
    rocket.items.append(item)
    rocket.filled_weight += item.mass
    rocket.filled_volume += item.volume
    if (rocket.payload_volume - rocket.filled_volume != 0):
        rocket.average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)
    else:
        rocket.average_density = 0


def remove_item_from_rocket(item, rocket):
    rocket.filled_weight -= item.mass
    rocket.filled_volume -= item.volume
    rocket.items.remove(item)
    rocket.average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)


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

    for rocket in rockets:
        for item in rocket.items:
            print(item)
        print(rocket.payload_mass - rocket.filled_weight)
        print(rocket.payload_volume - rocket.filled_volume)

    total_cost = 0
    for rocket in rockets:
        Fuel_grams = (rocket.mass + rocket.filled_weight)*(rocket.fuel_to_weight)/(1 - rocket.fuel_to_weight)
        cost_rocket = (rocket.base_cost * (10**6)) + round(1000 * Fuel_grams)
        print(cost_rocket)
        total_cost += cost_rocket
    return total_cost


if __name__ == "__main__":

    while(len(cargo_in_rockets) < 96):
        cargo_in_rockets =[]
        rockets = ReadRockets('rockets.csv')
        cargolist = ReadCargo('CargoLists/CargoList1.csv')

        shuffle(cargolist)
        fill_cargo(rockets, cargolist)
        print(len(set(cargo_in_rockets)))

        # cargo_unfilled = []
        # for item in cargolist:
        #     if item not in cargo_in_rockets:
        #         cargo_unfilled.append(item)
        #
        # switchitems_rockets(rockets)
        # # print(len(set(cargo_in_rockets)))
        # print(len(set(cargo_in_rockets)))
        # check_if_correct(rockets)
        #
        # check_items_rocket_cargo(rockets, cargolist)

        # cargo_unfilled = []
        # for item in cargolist:
        #     if item not in cargo_in_rockets:
        #         cargo_unfilled.append(item)

        # switchitems_rocket_and_unfilled(rockets, cargo_unfilled)
        #
        # check_if_correct(rockets)
        # print(len(set(cargo_in_rockets)))

    # for rocket in rockets:
    #     for item in rocket.items:
    #         print(item)
    #     print(rocket.payload_mass - rocket.filled_weight)
    #     print(rocket.payload_volume - rocket.filled_volume)

    summary(rockets)

    # cargo_unfilled = []
    # for item in cargolist:
    #     if item not in cargo_in_rockets:
    #         cargo_unfilled.append(item)
    #
    # switchitems_rockets(rockets)
    # cargo_test = cargo_in_rockets + cargo_unfilled
    #
    #
    # print(len(set(cargo_in_rockets)))
    #
    # cargo_unfilled = []
    # for item in cargolist:
    #     if item not in cargo_in_rockets:
    #         cargo_unfilled.append(item)

    # cargo_test = cargo_in_rockets + cargo_unfilled
    #
    # print(len(set(cargo_unfilled)))
    # print(len(set(cargo_test)))

    # switchitems_rocket_and_unfilled(rockets, cargo_unfilled)

    # print(len(cargo_in_rockets))

    # fitlastitems()

    # mass_items_unfilled = 0
    # volume_items_unfilled = 0
    # for item in cargo_unfilled:
    #     mass_items_unfilled += item.mass
    #     volume_items_unfilled += item.volume
    # print(mass_items_unfilled)
    # print(volume_items_unfilled)

    # cargo_unfilled = []
    # for item in cargolist:
    #     if item not in cargo_in_rockets:
    #         cargo_unfilled.append(item)
    #
    # # cargo_in_rockets_mass = 0
    # # cargo_in_rockets_volume = 0
    # # for item in cargo_in_rockets:
    # #     cargo_in_rockets_mass += item.mass
    # #     cargo_in_rockets_volume += item.volume
    #
    # check_if_correct(rockets)
    #
    # # print(cargo_in_rockets_mass)
    # # print(cargo_in_rockets_volume)
    #
    # mass_cargolist = 0
    # volume_cargolist = 0
    # for item in cargolist:
    #     mass_cargolist += item.mass
    #     volume_cargolist += item.volume
    #
    # # print('cargolist')
    # # print(mass_cargolist)
    # # print(volume_cargolist)
    #
    #
    #
    # mass_items_unfilled = 0
    # volume_items_unfilled = 0
    # for item in cargo_unfilled:
    #     mass_items_unfilled += item.mass
    #     volume_items_unfilled += item.volume
    #
    # # print('unfilled')
    # # print(mass_items_unfilled)
    # # print(volume_items_unfilled)
    #
    # total_cost = total_cost(rockets)
    #
    # print(total_cost)

    # for item in cargo_unfilled:
    #     print(item)
