from AirportVisit import AirportVisit


class ImpossibleRouteError(Exception):
    def __init__(self, message):
        self.message = message


class Route:
    """
    Route: Contains information about a possible route.
    Includes a method for calculating the cheapest places to refuel along the route.
    Also includes a method that generates a line for the csv file, and methods for
    printing information to the console.
    """
    def __init__(self, route, aircraft_range, airport_atlas, currency_table,
                 empty_tank=False, total_cost_of_stopovers=0):
        self.__fuel_capacity = aircraft_range
        self.airport_atlas = airport_atlas
        self.currency_table = currency_table
        self.__empty_tank = empty_tank
        self.__total_cost_of_stopovers = total_cost_of_stopovers
        self.__list_of_stops = self.__build_list_of_stops(route)
        self.__total_cost, self.__unused_fuel, self.__net_cost = self.calculate_cheapest_place_to_refuel()

    def __build_list_of_stops(self, route):
        output = []
        for i in range(len(route)):
            airport_code = route[i]
            country = self.airport_atlas.get_country(airport_code)
            fuel_price = self.currency_table.get_exchange_rate(country)
            if i == len(route) - 1:
                distance_to_next_airport = self.airport_atlas.get_distance_between_airports(route[i], route[0])
            else:
                distance_to_next_airport = self.airport_atlas.get_distance_between_airports(route[i], route[i + 1])
            if distance_to_next_airport > self.__fuel_capacity:
                return []
            output.append(AirportVisit(airport_code, fuel_price, distance_to_next_airport, self.__fuel_capacity))
        if output == []:
            raise ImpossibleRouteError("Cannot complete this route")
        return output

    def calculate_cheapest_place_to_refuel(self):
        if self.__list_of_stops == []:
            raise ImpossibleRouteError("Cannot complete this route")
        total_cost = 0
        valid_airports = []

        for i in range(len(self.__list_of_stops)):
            current_stop = self.__list_of_stops[i]
            valid_airports += [current_stop]          # the set of airports from which we can buy fuel for the next leg
            fuel_needed = current_stop.distance_to_next_airport

            # buy enough fuel for next leg
            while True:
                lowest_fuel_price = 10 ** 10
                for airport in valid_airports:
                    if airport.fuel_price <= lowest_fuel_price:
                        cheapest_airport = airport
                        lowest_fuel_price = airport.fuel_price
                        spare_fuel_capacity = airport.get_spare_fuel_capacity()

                if spare_fuel_capacity >= fuel_needed:
                    quantity_purchased = fuel_needed
                    cheapest_airport.buy_fuel(quantity_purchased)
                    for airport in valid_airports:
                        airport.add_fuel(quantity_purchased)
                    # eliminate airports where tank is full
                    valid_airports = [x for x in valid_airports if float(x.get_spare_fuel_capacity()) > 0]
                    total_cost += quantity_purchased * cheapest_airport.fuel_price
                    break

                else:                                                              # spare_fuel_capacity < fuelNeeded
                    quantity_purchased = spare_fuel_capacity
                    cheapest_airport.buy_fuel(quantity_purchased)
                    total_cost += quantity_purchased * cheapest_airport.fuel_price
                    fuel_needed -= quantity_purchased
                    for airport in valid_airports:
                        airport.add_fuel(quantity_purchased)
                    # eliminate airports where tank is full
                    valid_airports = [x for x in valid_airports if float(x.get_spare_fuel_capacity()) > 0]

        if self.__empty_tank:
            net_cost = total_cost + self.__total_cost_of_stopovers
            return total_cost, 0, net_cost + self.__total_cost_of_stopovers
        else:
            # buy extra fuel at cheapest airports
            extra_fuel = 0
            home_airport = self.__list_of_stops[0]
            while True:
                lowest_fuel_price = 10 ** 10
                for airport in valid_airports:
                    if airport.fuel_price <= lowest_fuel_price:
                        cheapest_airport = airport
                        lowest_fuel_price = airport.fuel_price
                        spare_fuel_capacity = airport.get_spare_fuel_capacity()
                if cheapest_airport.fuel_price < home_airport.fuel_price:
                    # print("buying from ", cheapest_airport.airport_code)
                    quantity_purchased = spare_fuel_capacity
                    cheapest_airport.buy_fuel(quantity_purchased)
                    extra_fuel += quantity_purchased
                    total_cost += quantity_purchased * cheapest_airport.fuel_price
                    for airport in valid_airports:
                        airport.add_fuel(quantity_purchased)
                    # eliminate airports where tank is full on departure
                    valid_airports = [x for x in valid_airports if float(x.get_spare_fuel_capacity()) > 0]
                    if len(valid_airports) == 0:
                        break
                else:
                    break
            net_cost = total_cost - (extra_fuel * home_airport.fuel_price) + self.__total_cost_of_stopovers
            return total_cost, extra_fuel, net_cost

    def get_cost_of_route(self):
        return self.__net_cost

    def __str__(self):
        output = "\n              Distance to          Fuel             Fuel           Total Fuel  \n"
        output += "  Airport     Next Airport       Purchase           Price            Spend\n"
        output += "                                                   (euros)          (euros)\n"
        for i in self.__list_of_stops:
            output += str(i) + "\n"
        return output

    def print_costs(self):
        print()
        print("Total fuel spend:                     €", "{:11,.2f}".format(self.__total_cost))
        print("Total cost of extra stopovers:        €", "{:11,.2f}".format(self.__total_cost_of_stopovers))
        print("Minus value of fuel brought home:     €", "{:11,.2f}".format(self.__unused_fuel * -1 *
                                                                            self.__list_of_stops[0].fuel_price)), ")"
        print("                                      =============")
        print("Net cost:                             €", "{:11,.2f}".format(self.__net_cost))

    def make_csv_row(self):
        row = []
        row.append("{:,.2f}".format(self.__net_cost))
        row.append("{:,.2f}".format(self.__unused_fuel * self.__list_of_stops[0].fuel_price))
        row.append("{:,.2f}".format(self.__total_cost_of_stopovers))
        row.append("{:,.2f}".format(self.__total_cost))
        for airport in self.__list_of_stops:
            row.append(airport.airport_code)
            row.append("{:,.2f}".format(airport.get_total_fuel_purchase()))
        return row
