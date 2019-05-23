import pandas as pd

class Item():
    def __init__(self, parcel_ID, mass, volume, density):
        """
        Initialize an Item
        """
        self.parcel_ID = parcel_ID
        self.mass = mass
        self.volume = volume
        self.density = density
        self.destination = 0

    def __str__(self):
        return self.parcel_ID

cygnus = ['CL1#55', 'CL1#65', 'CL1#71', 'CL1#60', 'CL1#47', 'CL1#3', 'CL1#5', 'CL1#24', 'CL1#75', 'CL1#83', 'CL1#98', 'CL1#15', 'CL1#44', 'CL1#37', 'CL1#46', 'CL1#54', 'CL1#67', 'CL1#94', 'CL1#63', 'CL1#92', 'CL1#70', 'CL1#7', 'CL1#99']

progress = ['CL1#52', 'CL1#12', 'CL1#69', 'CL1#87', 'CL1#9', 'CL1#97', 'CL1#22', 'CL1#36', 'CL1#72', 'CL1#2', 'CL1#39', 'CL1#4', 'CL1#56', 'CL1#61', 'CL1#20', 'CL1#80']

kounotori = ['CL1#89', 'CL1#42', 'CL1#51', 'CL1#86', 'CL1#79', 'CL1#58', 'CL1#78', 'CL1#11', 'CL1#13',  'CL1#30', 'CL1#10', 'CL1#40', 'CL1#1', 'CL1#33', 'CL1#81', 'CL1#16', 'CL1#35', 'CL1#50', 'CL1#45', 'CL1#38', 'CL1#62', 'CL1#59', 'CL1#17', 'CL1#93', 'CL1#95', 'CL1#48', 'CL1#100']

dragon = ['CL1#68', 'CL1#27', 'CL1#88', 'CL1#66', 'CL1#73', 'CL1#64', 'CL1#76', 'CL1#23', 'CL1#85', 'CL1#49', 'CL1#8', 'CL1#31', 'CL1#32', 'CL1#14', 'CL1#90', 'CL1#26', 'CL1#19', 'CL1#28', 'CL1#34', 'CL1#41', 'CL1#84', 'CL1#82', 'CL1#18', 'CL1#43', 'CL1#91', 'CL1#77', 'CL1#29', 'CL1#25', 'CL1#21', 'CL1#74', 'CL1#6']

# read in the cargolist from csv
def ReadCargo(INPUT_CSV):
    cargolist = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        item = Item(row['parcel_ID'], row['mass (kg)'], row['volume (m^3)'], row['mass (kg)']/row['volume (m^3)'])
        cargolist.append(item)
    return cargolist

cargolist = ReadCargo('CargoLists/CargoList1.csv')

def check_mass_and_volume(rocket):
    total_mass = 0
    total_volume = 0
    for item1 in rocket:
        for item2 in cargolist:
            if item1 == item2.parcel_ID:
                total_mass += item2.mass
                total_volume += item2.volume
    print(total_mass)
    print(total_volume)

if __name__ == "__main__":
    check_mass_and_volume(cygnus)
    check_mass_and_volume(progress)
    check_mass_and_volume(kounotori)
    check_mass_and_volume(dragon)
