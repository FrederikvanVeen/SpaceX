# import numpy as np
import pandas as pd
import math
# import random
from rocket import Rocket
from item import Item
# import algorithms as al
# import copy
# from matplotlib import pyplot as plt
# import time
# import csv


class Solution():

    def __init__(self, number):
        """
        Initialize a Rocket
        """
        self.rockets = self.ReadRockets("data/rockets.csv")
        self.cargolist = self.ReadCargo(f"data/CargoLists/CargoList{number}.csv")
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

    # counts items that are in rockets
    def count_items(self):
        self.items_count = len(self.cargo_in_rockets)
        print(self.items_count)

    # method to check if mass and volume is correct
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

    # calculates what mass and volume is not used
    def check_mass_volume_unused(self):
        for rocket in self.rockets:
            unused_mass = rocket.payload_mass - rocket.filled_weight
            unused_volume = rocket.payload_volume - rocket.filled_volume
            print(rocket.spacecraft)
            print(unused_mass)
            print(unused_volume)

    # calculate total cost of rockets used
    def calculate_cost(self):
        total_cost = 0
        base_cost_total = 0
        for rocket in self.rockets:
            base_cost_total += rocket.base_cost
            Fuel_grams = (rocket.mass + rocket.filled_weight)*(rocket.fuel_to_weight)/(1 - rocket.fuel_to_weight)
            # print(Fuel_grams)
            cost_rocket = (rocket.base_cost * (10**6)) + round(1000 * Fuel_grams)
            total_cost += cost_rocket
        self.cost = total_cost
