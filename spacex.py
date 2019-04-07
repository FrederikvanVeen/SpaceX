import numpy as np
import pandas as pd

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


def ReadRockets(INPUT_CSV):
    rockets = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        rocket = Rocket(row["Spacecraft"], row["Nation"], row['Payload Mass (kgs)'], row['Payload Volume (m3)'],row['Mass (kgs)'], row['Base Cost($)'], row['Fuel-to-Weight'], row['Payload Mass (kgs)']/row['Payload Volume (m3)'], [], 0, 0)
        rockets.append(rocket)
    return rockets


def ReadCargo(INPUT_CSV):
    cargolist = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        item = Item(row['parcel_ID'], row['mass (kg)'], row['volume (m^3)'], row['mass (kg)']/row['volume (m^3)'])
        cargolist.append(item)
    return cargolist


def fill_cargo(rockets, cargolist):
    filled_items =[]
    for i in range(3):
        for i in np.arange(0, 1, 0.1):
            for item in cargolist:
                for rocket in rockets:
                    rocket_density_upper = (rocket.average_density + rocket.average_density*i)
                    rocket_density_lower = (rocket.average_density - rocket.average_density*i)
                    if(item.density <= rocket_density_upper and item.density >= rocket_density_lower) and (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in filled_items):
                        load_item_in_rocket(item, rocket)
                        filled_items.append(item)
    return filled_items

def fitlastitems(rockets, cargolist):
    for item in cargolist:
        for rocket in rockets:
            if (rocket.filled_weight + item.mass <= rocket.payload_mass) and (rocket.filled_volume + item.volume <= rocket.payload_volume) and (item not in filled_items):
                load_item_in_rocket(item, rocket)
                filled_items.append(item)




def load_item_in_rocket(item, rocket):
    rocket.items.append(item)
    rocket.filled_weight += item.mass
    rocket.filled_volume += item.volume
    rocket.average_density = (rocket.payload_mass - rocket.filled_weight)/(rocket.payload_volume - rocket.filled_volume)


if __name__ == "__main__":
    rockets = ReadRockets('rockets.csv')
    cargolist = ReadCargo('CargoLists/CargoList1.csv')
    filled_items = fill_cargo(rockets, cargolist)

    cargofilled = 0
    for rocket in rockets:
        cargofilled += len(rocket.items)
    print(cargofilled)

    cargo_unfilled = []
    for item in cargolist:
        if item not in filled_items:
            cargo_unfilled.append(item)
    print(len(cargo_unfilled))

    # for rocket in rockets:
    #     print(rocket.payload_mass - rocket.filled_weight)
    #     print(rocket.payload_volume - rocket.filled_volume)

    fitlastitems(rockets, cargo_unfilled)

    cargofilled = 0
    for rocket in rockets:
        cargofilled += len(rocket.items)
    print(cargofilled)
