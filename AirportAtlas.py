from Airport import Airport
from math import sin, cos, acos, pi
import csv
EARTH_RADIUS = 6371


class AirportAtlas:
    """
    AirportAtlas class: stores airport objects in a dictionary,
    the key to which is the three-letter IATA airport code.
    This class contains several accessor methods for getting information
    about airports.

    Input: a csv file with the following columns:
    Column 2: Airport name.
    Column 4: Country.
    Column 5: IATA code.
    Column 6: Latitude.
    Column 7: Longitude.
    """

    def __init__(self, csv_file="input files/airport.csv"):
        self.__dictionary = self.__build_airport_dict(csv_file)

    def __build_airport_dict(self, csv_file):
        dictionary = {}
        with open(csv_file, 'rt', encoding="utf8") as f:
            reader = list(csv.reader(f))
            for row in reader:
                key = row.pop(4)
                dictionary[key] = Airport(key, row[1], row[3], row[5], row[6])
        return dictionary

    def is_in_airport_dictionary(self, airport_code):
        if airport_code in self.__dictionary:
            return True
        else:
            return False

    def get_country(self, code):
        return self.__dictionary[code].get_country()

    @staticmethod
    def great_circle_dist(lat1, long1, lat2, long2):
        """
        Calculates the great circle distance between two locations.

        Inputs: the latitude and longitude coordinates of the two locations (floats).
        Output: the distance in kilometers (float).
        """
        # calculate phi and theta for each location
        phi1 = (90 - lat1) * 2 * pi / 360
        theta1 = long1 * 2 * pi / 360
        phi2 = (90 - lat2) * 2 * pi / 360
        theta2 = long2 * 2 * pi / 360
        # calculate and return the distance
        return float(EARTH_RADIUS * acos((sin(phi1) * sin(phi2) * cos(theta1 - theta2)) + cos(phi1) * cos(phi2)))

    def get_distance_between_airports(self, code1, code2):
        """
        Returns the great circle distance between two airports.

        Inputs: two IATA airport codes (strings).
        Output: the distance in kilometers (float).
        """
        lat1, long1 = self.__dictionary[code1].get_coordinates()
        lat2, long2 = self.__dictionary[code2].get_coordinates()
        return self.great_circle_dist(lat1, long1, lat2, long2)

    def __str__(self):
        string = "This atlas contains " + str(len(self.__dictionary)) + " airports"
        return string

    # @staticmethod
    # def get_sector(latitude, longitude):
    #     lat = floor(latitude)
    #     long = floor(longitude)
    #     return lat, long
    #
    # def build_sector_dict(self):
    #     dictionary = {}
    #     for key in self.__dictionary:
    #         airport = self.__dictionary[key]
    #         airport_code = key
    #         latitude, longitude = airport.get_coordinates()
    #         latitude, longitude = floor(latitude), floor(longitude)
    #         if latitude in dictionary.keys():
    #             if longitude in dictionary[latitude]:
    #                 dictionary[latitude][longitude].append(airport_code)
    #             else:
    #                 dictionary[latitude][longitude] = [airport_code]
    #         else:
    #             dictionary[latitude] = {longitude: [airport_code]}
    #     return dictionary
    #
    # @staticmethod
    # def get_midpoint(lat1, long1, lat2, long2):
    #     # using the formula http://mathforum.org/library/drmath/view/51822.html
    #     long_difference = long2 - long1
    #     b_x = cos(lat2) * cos(long_difference)
    #     b_y = cos(lat2) * sin(long_difference)
    #     midpoint_lat = atan2(sin(lat1) + sin(lat2), ((cos(lat1) + b_x) * (cos(lat1) + b_x) + b_y ** 2) ** 0.5)
    #     midpoint_long = long1 + atan2(b_y, cos(lat1) + b_x)
    #     return degrees(midpoint_lat), degrees(midpoint_long)
    #
    # def get_midpoint_between_airports(self, code1, code2):
    #     """
    #     Returns the midpoint between two airports along the great circle.
    #
    #     Inputs: two IATA airport codes (strings).
    #     Output: the latitude and longitude coordinates of the midpoint (floats).
    #     """
    #     lat1, long1 = self.__dictionary[code1].get_coordinates()
    #     lat2, long2 = self.__dictionary[code2].get_coordinates()
    #     return self.get_midpoint(lat1, long1, lat2, long2)
    #
    # def get_closest_airports_to_a_location(self, latitude, longitude, number_of_airports=20):
    #     sector_lat, sector_long = AirportAtlas.get_sector(latitude, longitude)
    #     print("Getting closest airports", latitude, longitude)
    #     i = 0
    #     airport_list = []
    #     while len(airport_list) < number_of_airports:
    #         print(i)
    #         if i >= 10:
    #             return None
    #         airport_list = []
    #         for latitude in range(sector_lat - i, sector_lat + 1 + i):
    #             if latitude in self.__sector_dict.keys():
    #                 for longitude in range(sector_long - i, sector_long + 1 + i):
    #                     if longitude in self.__sector_dict[latitude]:
    #                         for airport_code in self.__sector_dict[latitude][longitude]:
    #                             airport_list.append(airport_code)
    #         i += 1
    #     return airport_list


def main():
    my_atlas = AirportAtlas('airport.csv')
    print(my_atlas.get_country('KBL'))
    print(my_atlas.get_distance_between_airports('JAA', 'JAA'))

if __name__ == '__main__':
    main()
