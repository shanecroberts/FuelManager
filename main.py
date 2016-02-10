"""
This is the mainline program, which is launched from the GUI.
It has two main functions:
    * manage_single_route() takes an itinerary that was input via the GUI and calculates the fuel purchase strategy.
    * manage_list_of_routes() takes a list of itineraries as its input and manages the fuel purchase strategy for all
    itineraries in the list.
"""
from CurrencyTable import CurrencyTable, CountryCurrencyFileError, ExchangeRateFileError
from AirportAtlas import AirportAtlas
from ItineraryRoster import ItineraryRoster
from Itinerary import Itinerary
from AircraftCatalog import AircraftCatalog
from time import strftime
from tkinter import messagebox
import os, csv


def manage_list_of_routes(real_exch_rates=True,
                          append_date_time=True,
                          empty_tank=False,
                          hubs=[],
                          stopover_cost=0,
                          itinerary_file="input files/testroutes.csv",
                          airport_file="input files/airport.csv",
                          aircraft_file="input files/aircraft.csv",
                          currency_file="input files/countrycurrency.csv",
                          exchange_rate_file="input files/currencyrates.csv",
                          output_file="bestroutes/bestroutes.csv"):

    # read data from input files and handle errors reading the files
    try:
        airport_atlas = AirportAtlas(airport_file)
    except FileNotFoundError:
        title = "File not found"
        message = "Unable to open the file: " + str(airport_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    try:
        currency_table = CurrencyTable(currency_file, exchange_rate_file,
                                   real_exch_rates)
    except CountryCurrencyFileError:
        title = "Unable to find the currency file"
        message = "Unable to open the file: " + str(currency_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    except ExchangeRateFileError:
        title = "Unable to find the currency file"
        message = "Unable to open the file: " + str(exchange_rate_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    try:
        aircraft_catalogue = AircraftCatalog(aircraft_file)
    except FileNotFoundError:
        title = "File not found"
        message = "Unable to open the file: " + str(aircraft_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    try:
        itinerary_roster = ItineraryRoster(airport_atlas, currency_table, aircraft_catalogue, itinerary_file, output_file,
                                       append_date_time, empty_tank, hubs, stopover_cost)
    except FileNotFoundError:
        title = "File not found"
        message = "Unable to open the file: " + str(itinerary_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None

    # calculate the best routes and output the results
    itinerary_roster.get_cheapest_routes()
    itinerary_roster.write_to_csv()


def manage_single_route(home_airport,
                        other_airports,
                        aircraft_code,
                        real_exch_rates=True,
                        append_date_time=True,
                        empty_tank=False,
                        hubs=[],
                        stopover_cost=0,
                        constraints=[],
                        airport_file="input files/airport.csv",
                        aircraft_file="input files/aircraft.csv",
                        currency_file="input files/countrycurrency.csv",
                        exchange_rate_file="input files/currencyrates.csv",
                        output_file="bestroutes/bestroutes.csv"):
    airport_list = [home_airport] + other_airports

    # read data from input files and handle errors reading the files
    try:
        airport_atlas = AirportAtlas(airport_file)
    except FileNotFoundError:
        title = "File not found"
        message = "Unable to open the file: " + str(airport_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    try:
        currency_table = CurrencyTable(currency_file, exchange_rate_file, real_exch_rates)
    except CountryCurrencyFileError:
        title = "Unable to find the currency file"
        message = "Unable to open the file: " + str(currency_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    except ExchangeRateFileError:
        title = "Unable to find the currency file"
        message = "Unable to open the file: " + str(exchange_rate_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    try:
        aircraft_catalogue = AircraftCatalog(aircraft_file)
    except FileNotFoundError:
        title = "File not found"
        message = "Unable to open the file: " + str(aircraft_file) + "\nPlease check the file path and try again"
        messagebox.showerror(title, message)
        return None
    try:
        aircraft_range = aircraft_catalogue.get_aircraft_range(aircraft_code)
    except KeyError:
        title = "Invalid aircraft code"
        message = "Unable to find the aircraft code " + str(aircraft_code) + "\nPlease check the code and try again"
        messagebox.showerror(title, message)
        return None

    # calculate the best route and output the result
    itinerary = Itinerary(airport_atlas, currency_table, airport_list, aircraft_code,
                          aircraft_range, empty_tank, hubs, stopover_cost, constraints)
    print(itinerary)
    itinerary.get_cheapest_route()
    if itinerary.get_error_message() is None:
        output_file = make_output_filename(output_file, append_date_time)
        write_to_csv(output_file, itinerary.cheapest_route.make_csv_row())


def make_output_filename(output_file, append_date_time):
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


def write_to_csv(output_file, csv_data):
    with open(os.path.join(output_file), "wt", newline="") as f:
        writer = csv.writer(f, delimiter=",")
        writer.writerow(["Net fuel cost", "Value of fuel brought home", "Total cost of stopovers",
                         "Total fuel purchase", "Home airport", "Fuel purchase", "Airport", "Fuel purchase",
                         "Airport", "Fuel purchase", "Airport", "Fuel purchase", "Airport", "Fuel purchase"])
        writer.writerow(csv_data)
    print("Report successfully saved to", output_file)

if __name__ == '__main__':
    manage_list_of_routes()
