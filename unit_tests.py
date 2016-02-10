from Itinerary import Itinerary
from AirportAtlas import AirportAtlas
from CurrencyTable import CurrencyTable, CountryCurrencyFileError
from AircraftCatalog import AircraftCatalog
from main import manage_single_route
from Route import ImpossibleRouteError
import unittest

class TestAirportAtlas(unittest.TestCase):
    test_atlas = AirportAtlas('input files/airport.csv')
    test_aircraft_catalog = AircraftCatalog('input files/aircraft.csv')
    test_currency_table = CurrencyTable()
    airport_list = ['JAA', 'AAL', 'DUB', 'JFK', 'SYD']
    test_itinerary = Itinerary(test_atlas, test_currency_table, airport_list, '737', 15000)
    valid_constraints = [['JFK', 'AAL'], ['SYD', 'DUB', 'JFK'], ['SYD', 'JAA', 'JFK']]
    invalid_constraints = [['AAL'], ['JAA', 'JFK', 'SYD', 'AAL'], ['ABC', 'DEF']]
    currency_file = 'input files/countrycurrentzy.csv'
    exchange_rate_file = 'input files/currencyrates.csv'
    known_ranges = [['A330', 13430], ['A319', 3750], ['777', 15610]]
    invalid_ranges = [['13430', 13430], ['A3191', 3750], ['Spruce Goose', 15610]]
    impossible_routes = (("DUB", ["LHR", "SYD"], "747"), ("JFK", ["ICN", "SYD"], "BAE146"))
    known_distances = (('JAA', 'AAL', 5120.472011364758), ('DUB', 'AAL', 1096.7379627823607), ('JAA', 'JFK', 10904.683283307477), ('SYD', 'LHR', 17020.25673366721))

    def test_that_method_correctly_identifies_valid_constraints(self):
        """
        The is_valid_constraint() method should return True for valid constraints.
        """
        for constraint in self.valid_constraints:
            result = self.test_itinerary.is_valid_constraint(constraint, self.airport_list)
            self.assertEqual(result, True)

    def test_that_method_correctly_identifies_invalid_constraints(self):
        """
        The is_valid_constraint() method should return False for invalid constraints.
        """
        for constraint in self.invalid_constraints:
            result = self.test_itinerary.is_valid_constraint(constraint, self.airport_list)
            self.assertEqual(result, False)

    def test_raising_CountryCurrencyFileError(self):
        """
        Attempting to build a currency table with an invalid filename should raise a CountryCurrencyFileError.
        """
        with self.assertRaises(CountryCurrencyFileError):
            CurrencyTable(self.currency_file, self.exchange_rate_file)

    def test_raising_ImpossibleRouteError(self):
        """
        Attempting to manage a route beyond the aircraft's range should raise an ImpossibleRouteError.
        """
        for home_airport, other_airports, aircraft_code in self.impossible_routes:
            result = manage_single_route(home_airport, other_airports, aircraft_code)
            self.assertRaises(ImpossibleRouteError)

    def test_get_aircraft_range_method_with_known_ranges(self):
        for aircraft, range in self.known_ranges:
            result = int(self.test_aircraft_catalog.get_aircraft_range(aircraft))
            self.assertEqual(result, range)

    def test_get_distance_between_airports_method_using_known_values(self):
        for airport1, airport2, distance in self.known_distances:
            result = self.test_atlas.get_distance_between_airports(airport1, airport2)
            self.assertEqual(result, distance)

    def test_that_the_distance_between_an_airport_and_itself_is_zero(self):
        for airport_code in self.airport_list:
            result = int(self.test_atlas.get_distance_between_airports(airport_code, airport_code))
            self.assertEqual(result, 0)

    def test_getting_all_possible_permutations_of_a_route(self):
        """
        The number of possible routes from a list of five airports is 384.

        The number of permutations of a list with four non-home airports is 24 (= 4!).
        Each of the five airports, including the home airport, can be revisited at three points in each route,
        and there is also the option of not revisiting any of the airports in the route, so there are 16 potential
        routes for each of the 24 permutations.
        16 * 24 = 384
        """
        result = self.test_itinerary.build_route_list()
        self.assertEqual(len(result), 384)

if __name__ == '__main__':
    unittest.main()
