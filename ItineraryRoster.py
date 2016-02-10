from Itinerary import Itinerary
import csv, os
from time import strftime

class ItineraryRoster:
    """
    ItineraryRoster: reads itineraries from a csv file and stores them as Itinerary objects in a list.
    Also contains a method for writing the program output to a csv file.
    """

    def __init__(self, airport_atlas, currency_table, aircraft_catalogue,
                 input_file='testroutes.csv', output_file='bestroutes/bestroutes.csv',
                 append_date_time=True, empty_tank=False, hubs=[], stopover_cost=0):
        self.aircraft_catalogue = aircraft_catalogue
        self.airport_atlas = airport_atlas
        self.currency_table = currency_table
        self.empty_tank = empty_tank
        self.hubs = hubs
        self.stopover_cost = stopover_cost
        self.itinerary_list = self.build_itinerary_list(input_file)
        self.output_file = self.make_output_filename(output_file, append_date_time)
        # self.write_to_csv()

    def build_itinerary_list(self, inputFile):
        itineraryList = []
        with open(inputFile, 'rt') as f:
            reader = list(csv.reader(f))
            for row in reader:
                # detect number of airports in row
                row_backwards = row[::-1]
                number_of_airports = len(row_backwards) - 1
                for i in range(len(row_backwards)):
                    if row_backwards[i] == "":
                        number_of_airports = len(row) - (i + 2)

                airport_list = []
                for i in range(number_of_airports):
                    airport_list.append(row[i].upper())
                aircraft_code = row[number_of_airports].upper()

                # try to get the aircraft range from aircraft_catalogue
                try:
                    aircraft_range = self.aircraft_catalogue.get_aircraft_range(aircraft_code)
                except KeyError:
                    aircraft_range = None
                new_itinerary = Itinerary(self.airport_atlas, self.currency_table,
                                          airport_list, aircraft_code, aircraft_range,
                                          self.empty_tank, self.hubs, self.stopover_cost)
                itineraryList.append(new_itinerary)
        return itineraryList

    def get_cheapest_routes(self):
        for itinerary in self.itinerary_list:
            print("\n", "*" * 75, sep="")
            print(itinerary)
            itinerary.get_cheapest_route()

    def make_output_filename(self, output_file, append_date_time):
        """
        If the append_date_time parameter is True, appends the current date and time to the filename.
        Otherwise returns the plain filename.
        """
        if append_date_time == False:
            return output_file
        else:
            date = strftime(" %Y%m%d %H%M%S")
            insertion_point = output_file.find(".")
            new_output_file = output_file[:insertion_point] + date + output_file[insertion_point:]
            return new_output_file

    def write_to_csv(self):
        with open(os.path.join(self.output_file), "wt", newline="") as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["Net fuel cost", "Value of fuel brought home", "Total cost of stopovers",
                             "Total fuel purchase", "Home airport", "Fuel purchase", "Airport", "Fuel purchase",
                             "Airport", "Fuel purchase", "Airport", "Fuel purchase", "Airport", "Fuel purchase"])
            for itinerary in self.itinerary_list:
                if itinerary.get_error_message() is not None:
                    writer.writerow([itinerary.get_error_message().replace("\n", " ")])
                else:
                    writer.writerow(itinerary.cheapest_route.make_csv_row())
        print("Report successfully saved to", self.output_file)
