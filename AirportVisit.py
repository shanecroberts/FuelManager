class AirportVisit:
    """
    A class for recording information about a planned stop at an airport.

    The class has two mutator methods, buy_fuel() and add_fuel(), and
    two accessor methods, get_spare_fuel_capacity() and get_total_fuel_purchase().
    """
    def __init__(self, airport_code, fuel_price, distance_to_next_airport, aircraft_range):
        self.airport_code = airport_code
        self.fuel_price = float(fuel_price)
        self.distance_to_next_airport = distance_to_next_airport
        self.fuel_capacity = float(aircraft_range)

        # fuel management attributes
        self.__total_fuel_purchase = 0
        self.__fuel_in_tank_on_departure = 0
        self.__spare_fuel_capacity = self.fuel_capacity

    def buy_fuel(self, quantity_purchased):
        """
        This mutator method increases the self.__total_fuel_purchase attribute whenever fuel is purchased at an airport.
        """
        self.__total_fuel_purchase += quantity_purchased

    def add_fuel(self, quantity_added):
        """
        This mutator method is invoked whenever fuel is purchased at an airport or at any subsequent airport within
        range of the current airport.  It decreases the amount of fuel that can be bought at the current airport.
        """
        self.__fuel_in_tank_on_departure += quantity_added
        self.__spare_fuel_capacity -= quantity_added
        if self.__spare_fuel_capacity < 0:
            self.__spare_fuel_capacity = 0

    def get_spare_fuel_capacity(self):
        return self.__spare_fuel_capacity

    def get_total_fuel_purchase(self):
        return self.__total_fuel_purchase

    def __str__(self):
        output = "    " + self.airport_code
        output += "        " + "{:9,.2f}".format(self.distance_to_next_airport)
        output += "       " + "{:9,.2f}".format(self.__total_fuel_purchase)
        output += "         " + "{:7,.2f}".format(self.fuel_price)
        output += "          " + "{:9,.2f}".format(self.__total_fuel_purchase * self.fuel_price)
        return output
