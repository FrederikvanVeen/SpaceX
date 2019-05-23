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

cygnus = [
'CL2#56',
'CL2#24',
'CL2#94',
'CL2#98',
'CL2#31',
'CL2#83',
'CL2#96',
'CL2#1',
'CL2#35',
'CL2#67',
'CL2#85',
'CL2#28',
'CL2#5',
'CL2#90',
'CL2#49',
'CL2#25',
'CL2#72',
'CL2#47',
'CL2#86',
'CL2#77'
]

progress = [
'CL2#8',
'CL2#75',
'CL2#58',
'CL2#29',
'CL2#44',
'CL2#53',
'CL2#52',
'CL2#60',
'CL2#45',
'CL2#22',
'CL2#71',
'CL2#64',
'CL2#76',
'CL2#80'
]

kounotori = [
'CL2#20',
'CL2#17',
'CL2#82',
'CL2#55',
'CL2#91',
'CL2#92',
'CL2#73',
'CL2#68',
'CL2#87',
'CL2#48',
'CL2#39',
'CL2#15',
'CL2#14',
'CL2#97',
'CL2#32',
'CL2#61',
'CL2#65',
'CL2#62',
'CL2#63',
'CL2#51',
'CL2#70',
'CL2#18',
'CL2#33',
'CL2#4',
'CL2#57'
]

dragon = ['CL2#12',
'CL2#100',
'CL2#10',
'CL2#2',
'CL2#3',
'CL2#21',
'CL2#13',
'CL2#41',
'CL2#88',
'CL2#36',
'CL2#27',
'CL2#59',
'CL2#93',
'CL2#84',
'CL2#7',
'CL2#26',
'CL2#9',
'CL2#37',
'CL2#30',
'CL2#74',
'CL2#11',
'CL2#99',
'CL2#54',
'CL2#78',
'CL2#81',
'CL2#19',
'CL2#46',
'CL2#6',
'CL2#66',
'CL2#69',
'CL2#40']

all = cygnus + progress + kounotori + dragon
print(len(set(all)))


# read in the cargolist from csv
def ReadCargo(INPUT_CSV):
    cargolist = []
    df = pd.read_csv(INPUT_CSV)
    for index, row in df.iterrows():
        item = Item(row['parcel_ID'], row['mass (kg)'], row['volume (m^3)'], row['mass (kg)']/row['volume (m^3)'])
        cargolist.append(item)
    return cargolist


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
    cargolist = ReadCargo('CargoLists/CargoList2.csv')
    check_mass_and_volume(cygnus)
    check_mass_and_volume(progress)
    check_mass_and_volume(kounotori)
    check_mass_and_volume(dragon)
