from Route import Route, ImpossibleRouteError
from itertools import permutations


class Itinerary:
    """
    A class to store a list of airports to be visited and an aircraft code.
    """
    def __init__(self, airport_atlas, currency_table, airport_list, aircraft_code, aircraft_range,
                 empty_tank=False, hubs=[], stopover_cost=0, constraints=[]):
        self.__airport_list = airport_list
        self.__aircraft_code = aircraft_code  # maybe don't need this
        self.__aircraft_range = aircraft_range
        self.__hubs = hubs
        self.__airport_atlas = airport_atlas
        self.__currency_table = currency_table

        # check inputs for errors
        if self.__aircraft_range is None:
            self.__error = "Unable to find the aircraft code " + str(self.__aircraft_code) + \
                           ".\nPlease check the code and try again."
        else:
            self.__error = None
        for airport in self.__airport_list:
            if not self.__airport_atlas.is_in_airport_dictionary(airport):
                self.__error = "Unable to find the airport code " + str(airport) + \
                               ".\nPlease check the code and try again."
        self.__constraints = self.get_valid_constraints(constraints, self.__airport_list)
        self.__empty_tank = empty_tank
        self.__route_list = []
        self.__stopover_cost = stopover_cost
        self.cheapest_route = 0
        self.__lowest_cost = 10 ** 10

    def add_an_optional_extra_stop(self, route):
        """
        Adds each possible fuel stop to a route.

        Parameter: a list of airports.
        Returns: a list containing every possible addition of one extra airport.

        Note: The home airport will always be the same.
        Any one airport, including the home airport, may be revisited once.
        """
        visitable_airports = route[:]
        for airport in self.__hubs:  # don't hard-code this
            if airport not in visitable_airports:
                visitable_airports.append(airport)
        output_list = [route]
        for position in range(len(route) - 1):
            for airport in visitable_airports:
                if airport != route[position] and airport != route[position + 1]:
                    new_list = route[:]
                    new_list.insert(position + 1, airport)
                    output_list.append(new_list)
        for airport in visitable_airports:
            if airport != route[0] and airport != route[-1]:
                new_list = route[:]
                new_list.append(airport)
                output_list.append(new_list)
        return output_list

    def build_route_list(self):
        """ Returns a list of every possible route for a given itinerary. """
        home_airport, *non_home_airports = self.__airport_list
        route_permutations = permutations(non_home_airports)  # get all permutations of non-home airports

        # add the optional extra fuel stop
        route_list = []
        for i in route_permutations:
            i = list(i)
            i.insert(0, home_airport)
            extra_fuel_stops = self.add_an_optional_extra_stop(i)
            for route in extra_fuel_stops:
                route_list.append(route)

        # apply __constraints
        if len(self.__constraints) > 0:
            route_list = self.apply_constraints(route_list, self.__constraints)
        return route_list

    def is_valid_constraint(self, constraint, airport_list):
        """ Checks whether a constraint is valid. """
        if not 2 <= len(constraint) <= 3:
            return False
        for airport in constraint:
            if airport not in airport_list:
                return False
        return True

    def get_valid_constraints(self, constraints, airport_list):
        """ Takes a list of constraints and filters out the invalid ones. """
        valid_constraints = []
        for constraint in constraints:

            # remove redundant airports
            if constraint[0] == airport_list[0]:
                constraint = constraint[1:]
            if constraint[-1] == airport_list[0]:
                constraint = constraint[:-1]

            if self.is_valid_constraint(constraint, airport_list):
                if constraint not in valid_constraints:
                    valid_constraints.append(constraint)
            else:
                print("Ignoring constraint: ", constraint)

        return valid_constraints

    def apply_constraints(self, route_list, constraints):
        valid_route_list = route_list                                # all routes that meet the constraints so far

        # iterate through all constraints, eliminating routes from valid_route_list
        for constraint in constraints:
            new_route_list = []

            if len(constraint) == 2:
                for route in valid_route_list:
                    airport0 = route.index(constraint[0])  # first visit to airport1
                    airport1 = (len(route) - 1) - route[::-1].index(constraint[1])  # last visit to airport2

                    # if route meets constraint, append to new_route_list
                    if airport0 < airport1:
                        new_route_list.append(route)

            elif len(constraint) == 3:
                for route in valid_route_list:
                    airport0 = route.index(constraint[0])  # first visit to airport1
                    airport2 = (len(route) - 1) - route[::-1].index(constraint[2])  # last visit to airport3

                    # if route meets constraint, append to new_route_list
                    if airport0 < airport2:
                        if constraint[1] in route[airport0 + 1:airport2]:
                            new_route_list.append(route)
            valid_route_list = new_route_list
        return valid_route_list

    def get_cheapest_route(self):
        # calculates the cost of each possible route and returns the cheapest route (and its cost)
        if self.__error is not None:                                  # if there are no valid routes for this itinerary
            return None, 10 ** 10
        lowest_cost = 10 ** 10                        # method will return this number if itinerary cannot be completed
        self.route_list = self.build_route_list()
        self.cheapest_route = None

        for route in self.route_list:
            total_cost_of_stopovers = self.__stopover_cost * (len(route) - len(self.__airport_list))
            try:
                current_route = Route(route,
                                      self.__aircraft_range,
                                      self.__airport_atlas,
                                      self.__currency_table,
                                      self.__empty_tank,
                                      total_cost_of_stopovers)
            except ImpossibleRouteError:
                continue                                              # this route has a leg that cannot be completed
            else:
                current_route_cost = current_route.get_cost_of_route()
                if current_route_cost < lowest_cost:
                    self.cheapest_route = current_route
                    lowest_cost = current_route_cost
        if lowest_cost == 10 ** 10:                                   # if itinerary cannot be completed
            print("Aircraft has insufficient range to complete this itinerary.")
            print("Consider using a larger aircraft or adding a fuel stop to the list of hubs.")
            self.__error = "Aircraft has insufficient range to complete this itinerary." \
                           "\nConsider using a larger aircraft or adding a fuel stop to the list of hubs."
            self.cheapest_route = None
        else:
            print()
            print(self.cheapest_route)
            self.cheapest_route.print_costs()
            print()
        self.lowest_cost = lowest_cost
        return self.cheapest_route, lowest_cost

    def get_error_message(self):
        """ Returns an error message explaining that the itinerary could not be completed. """
        return self.__error

    def __str__(self):
        output = "Airports: "
        for i in range(len(self.__airport_list) - 1):
            output += self.__airport_list[i] + ", "
        output += self.__airport_list[-1] + "\n"
        if self.__error is None:
            output += "Aircraft: " + str(self.__aircraft_code)
            output += " (range: " + "{:,.0f}".format(self.__aircraft_range) + " km)"
        else:
            output += str(self.__error)
        return output
