class Airport:
    """
    Airport class: holds information about an airport.

    Note: all attributes are private, but the airport's coordinates can be accessed via the
    accessor method get_coordinates(), and the airport country can be accessed via get_country()
    """

    def __init__(self, code, name, country, latitude, longitude):
        self.__code = code
        self.__name = name
        self.__country = country
        self.__lat = float(latitude)
        self.__long = float(longitude)

    def get_coordinates(self):
        """
        Returns two floating point numbers: the airport's latitude and longitude coordinates, respectively.
        """
        return self.__lat, self.__long

    def get_country(self):
        return self.__country

    def __str__(self):
        return " {} ({} in {}. Latitude: {}, longitude:{}.) ".format(self.__code, self.__name,
                                                                     self.__country, self.__lat, self.__long)


def main():
    my_airport = Airport('NOC', 'Ireland West Airport Knock', 'Ireland', 53.910278, -8.818611)
    print(my_airport)

if __name__ == '__main__':
    main()
