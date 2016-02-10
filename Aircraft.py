MILES_TO_KILOMETERS = 1.609344

class Aircraft:
    """
    Aircraft class.  Holds information about an aircraft_code.

    Note: all attributes are private, but the aircraft_code's range can be accessed via
    the accessor method get_aircraft_range().
    """
    def __init__(self, airplane_code, type, manufacturer, units, nonstandardised_range):
        self.__airplane_code = airplane_code
        self.__type = type
        self.__manufacturer = manufacturer
        self.__units = units.lower()
        self.__nonstandardised_range = float(nonstandardised_range)
        self.__range = self.__calc_range_in_metric()

    def __calc_range_in_metric(self):
        if self.__units == "imperial":
            return self.__nonstandardised_range * MILES_TO_KILOMETERS
        else:                                                                       # assume metric if no units given
            return self.__nonstandardised_range

    def get_aircraft_range(self):
        return self.__range

    def __str__(self):
        string = "The " + self.__manufacturer + " " \
                 + self.__airplane_code + " " \
                 + self.__type + " has a range of " \
                 + "{:,.2f}".format(self.__range) + " km"
        return string


def main():
    my_plane = Aircraft("Spruce Goose", 'flying boat', 'Hughes Aircraft', 'imperial', 3000)
    print(my_plane)

if __name__ == '__main__':
    main()