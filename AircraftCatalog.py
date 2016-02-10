from Aircraft import Aircraft
import csv

class AircraftCatalog:
    """
    AircraftCatalog class: holds information about types of aircraft_code.
    The information is stored in a dictionary, the key to which is the aircraft code.

    Input: a csv file with five columns:
    Column 1: Airplane code.
    Column 2: Aircraft type.
    Column 3: Units (metric or imperial).
    Column 4: Manufacturer.
    Column 5: Range (in km or miles).
    """

    def __init__(self, csvFile='aircraft_code.csv'):
        self.__dictionary = self.__build_aircraft_dict(csvFile)

    def __build_aircraft_dict(self, csvFile):
        """
        Builds a dictionary of airport objects.
        """
        dictionary = {}
        with open(csvFile, 'rt', encoding="utf8") as f:
            reader = list(csv.reader(f))
            for row in reader:
                if str(row[0]) != "code":
                    dictionary[row[0]] = Aircraft(row[0].upper(), row[1], row[3], row[2], row[4])
        return dictionary

    def get_aircraft_range(self, aircraft_code):
        aircraft = self.__dictionary[aircraft_code]
        return aircraft.get_aircraft_range()
