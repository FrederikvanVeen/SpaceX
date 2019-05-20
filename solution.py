import numpy as np
import pandas as pd
import math
import random
from rocket import Rocket
from item import Item
import algorithms as al
import copy

cargo_in_rockets =[]

class Solution():

    def __init__(self):
        """
        Initialize a Rocket
        """
        self.rockets = self.ReadRockets("rockets.csv")
        self.cargolist = self.ReadCargo("CargoLists/CargoList1.csv")
        self.items_count = 0
        self.cost = 0
        self.cargo_in_rockets = []


    # read in all the rockets from csv
    def ReadRockets(self, INPUT_CSV):
        rockets = []
        df = pd.read_csv(INPUT_CSV)
        for index, row in df.iterrows():
            rocket = Rocket(row["Spacecraft"], row["Nation"], row['Payload Mass (kgs)'], row['Payload Volume (m3)'],row['Mass (kgs)'], row['Base Cost($)'], row['Fuel-to-Weight'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], [], 0, 0, row['id'])
            rockets.append(rocket)
        return rockets


    # read in the cargolist from csv
    def ReadCargo(self, INPUT_CSV):
        cargolist = []
        df = pd.read_csv(INPUT_CSV)
        for index, row in df.iterrows():
            item = Item(row['parcel_ID'], row['mass (kg)'], row['volume (m^3)'], row['mass (kg)']/row['volume (m^3)'])
            cargolist.append(item)
        return cargolist


    def Items_count(self):
        self.items_count = len(self.cargo_in_rockets)
        print(self.items_count)


    def check_if_correct(self):
            total_filled_mass = 0
            total_filled_volume = 0
            total_volume_items = 0
            total_mass_items = 0
            for rocket in self.rockets:
                total_filled_mass += rocket.filled_weight
                total_filled_volume += rocket.filled_volume
                for item in rocket.items:
                    total_volume_items += item.volume
                    total_mass_items += item.mass
            print(total_filled_mass)
            print(total_mass_items)
            print(total_filled_volume)
            print(total_volume_items)


    def check_mass_volume_unused(self):
        for rocket in self.rockets:
            unused_mass = rocket.payload_mass - rocket.filled_weight
            unused_volume = rocket.payload_volume - rocket.filled_volume
            print(rocket.spacecraft)
            print(unused_mass)
            print(unused_volume)


    def cost_total(self):
        total_cost = 0
        for rocket in self.rockets:
            Fuel_grams = (rocket.mass + rocket.filled_weight)*(rocket.fuel_to_weight)/(1 - rocket.fuel_to_weight)
            print(Fuel_grams)
            cost_rocket = (rocket.base_cost * (10**6)) + round(1000 * Fuel_grams)
            total_cost += cost_rocket
        self.cost = total_cost
        print(self.cost)



if __name__ == "__main__":


    # solution solved by sim_an_hill_climber
    solution_1 = Solution()
    random.shuffle(solution_1.cargolist)
    al.sim_an_hill_climber_spacex(solution_1)
    solution_1_copy = copy.deepcopy(solution_1)
    solution_1.Items_count()
    solution_1.cost_total()
    cost_before = solution_1.cost
    al.sim_an_cost(solution_1, 500, 30)
    solution_1.cost_total()
    cost_after = solution_1.cost
    cost_dif = cost_after - cost_before
    print(cost_dif)

    solution_1_copy.cost_total()
    cost_before = solution_1_copy.cost
    al.greedy_cost(solution_1_copy)
    solution_1_copy.cost_total()
    cost_after = solution_1_copy.cost
    cost_dif = cost_after - cost_before
    print(cost_dif)
        


        # # solution_4.check_if_correct()
