class Rocket():
    def __init__(self, spacecraft, nation, payload_mass, payload_volume, mass, base_cost, fuel_to_weight, average_density, items, filled_weight, filled_volume, id):
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
        self.id = id

    def load_item(self, item):
        self.items.append(item)
        self.filled_weight += item.mass
        self.filled_volume += item.volume
        if (self.payload_volume - self.filled_volume != 0):
            self.average_density = (self.payload_mass - self.filled_weight)/(self.payload_volume - self.filled_volume)
        else:
            self.average_density = 0

    def interchange_items(self, item_i, item_j):
        self.filled_weight = self.filled_weight + item_j.mass - item_i.mass
        self.filled_volume = self.filled_volume + item_j.volume - item_i.volume

        for n in range(len(self.items)):
            if self.items[n] == item_i:
                self.items[n] = item_j

    def remove_item(self, item):
        self.items.remove(item)
        self.filled_weight -= item.mass
        self.filled_volume -= item.volume
        if (self.payload_volume - self.filled_volume != 0):
            self.average_density = (self.payload_mass - self.filled_weight)/(self.payload_volume - self.filled_volume)
        else:
            self.average_density = 0

    def __str__(self):
        return str(self.average_density)
