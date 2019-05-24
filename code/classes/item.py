class Item():
    def __init__(self, parcel_ID, mass, volume, density):
        """
        Initialize an Item
        """
        self.parcel_ID = parcel_ID
        self.mass = mass
        self.volume = volume
        self.density = density

    def __str__(self):
        return self.parcel_ID + '  ' + str(self.mass) + '  ' +  str(self.volume)
