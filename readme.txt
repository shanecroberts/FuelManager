== Project specification ==
This assignment was submitted as part of my Object-Oriented Programming module.  The assignment specification was:
“Imagine you work for a small Irish software company that has won the tender to deliver a fuel management software solution to a large Irish Airline. The airline is entering the European air freight cargo business and wants a software tool to manage their fuel purchasing strategy. Each week, an aircraft will fly up to six trips. The airplane will start and end in the same home airport each week and can optionally visit one other airport twice. The company has a number of different aircrafts that have different fuel capacities and the cost of fuel varies from airport to airport. Given a list of 5 airports (including to the home airport) that a given plane needs to visit in a week, the most economic route must be found.
* The distance between airports is calculated as the great circle distance between them
* The cost of fuel is assumed to be 1 euro per 1 litre at Airports where the currency is Euros
* The cost in of fuel in airports where the local currency is not euros is assumed to be the exchange rate from the local currency to euro. e.g. in you travel from London to Dublin and the exchange rate is GBP1 = EUR1.4029 and you purchase 1000 litres of fuel it will cost EUR1402.
The program with take file inputs and give file outputs using CSV formats. It should also have a basic GUI to allow input of an individual itinerary. At a minimum, the program should work with a command line interface to interact with the user – this is not necessary if you have file and/or GUI interfaces.”

== Definition of terms ==
Home airport: The airport where a journey starts and finishes.
Itinerary: A list of airports to be visited by a single aircraft in a single journey.  Includes a home airport and one or more other airports.  Unlike a route, this is an unordered list (except for the first airport in the list, which is always the home airport).
Route: An ordered list of the airports to be visited in a single journey.
Leg: a single flight.

== How to use this software ==
Run FuelManager.py to launch the graphical user interface.

== GUI Parameters ==
Use real-time exchange rates:
When this option is selected, the program will attempt to retrieve real-time exchange rates from Google Finance.  If the program cannot retrieve real-time exchange rate information, an error message will be printed to the console and the program will use the exchange rate from the file.  (For this reason, the program requires a list of exchange rates to be input, even when the real-time exchange rate option is selected.)  If the program fails to retrieve a real-time exchange rate from the internet, it will not attempt to look up that exchange rate again for the remainder of the program run.

Hubs:
A sensible fuel management strategy will take advantage of the fact certain airports have extremely low fuel prices.  By making a fuel stop in, say, Minsk, before a long-haul flight, the company can make considerable savings.
The user can add any number of hubs (three-letter airport codes, separated by a space) and the program will consider whether it is possible to save money by adding an extra fuel stop.

Constraints:
The users can specify that certain airports must be visited in a particular order, by imposing constraints on the route.  Enter constraints into the GUI by typing three-letter airport codes separated by spaces.  To enter more than one constraint, use “ / “ to separate them.
If a user enters a constraint that appears to be valid (that is, a three-character alphanumeric string) but doesn’t make sense (for example, it comprises the home airport and one other airport, or it includes an airport not in the itinerary) the program prints a message to the console and ignores the constraint.
Examples:
• JFK AAL AMS will visit the three airports in that order.
• JFK AAL / JFK AMS will visit JFK before both AAL and AMS
• JFK WWW will be ignored if WWW is not in the itinerary
There is no limit to the number of constraints that can be applied to a single route.

Cost of each extra stopover:
Because each additional fuel stop imposes costs on the company, this option allows the user to set a threshold below which it is not profitable to make an extra fuel stop.  (Ideally, the cost of a refuel stop should be input via a csv file, as the cost will vary depending on the airport and aircraft.)

Always return home with an empty tank:
When an aircraft visits a country with low fuel prices, the company can save considerable sums, and even make large profits, by filling the aircraft’s fuel tank to capacity and bringing the extra fuel home.  This fuel can be saved for the aircraft’s next journey, transferred to a different aircraft, or sold at the home country’s fuel price.
Should the user not wish to take advantage of this option, they can select “Always return home with an empty tank”.

Append date and time to filename:
To avoid overwriting files or prompting the user to provide a unique filename each time the program is run, the software automatically appends the current date and time to each filename.  The user can override this feature by unchecking the box.

The GUI also allows the user to select input files and choose where to save to output files.

== Inputs ==
In order to run, the program requires the following information:
•	A list of airports, including the airport name, country, IATA code and coordinates (latitude and longitude).
•	A list of aircraft types, including the aircraft code and the aircraft’s range.  By default, the aircraft’s range is assumed to be in kilometers, unless the aircraft’s “units” are imperial.
•	A list of countries and the currencies they use (three-letter currency code).
•	A list of exchange rates, including the three-letter currency code and value in euros of one unit of the currency.
By default, the input files are stored in a subdirectory called “input files” in the same directory as the program.  The specific information which must be contained in each column of each csv file is outlined in the docstring for the relevant program module (AirportAtlas, AircraftCatalog and CurrencyTable, respectively).
To manage a list of itineraries, the user must upload a csv file.  Each row in the csv file should represent a single itinerary.  Each cell in the row should be a three-letter IATA aircraft code, except the final cell, which is the aircraft code.  (The program automatically detects the number of airports in each itinerary.)

== Outputs ==
The program outputs the best route in two ways: by printing the information to the console, and by writing to a csv file.
Print to console:
The program displays a summary of each itinerary in the following format:
The program also displays any errors that occur during runtime.
Output to file:
The program automatically generates a csv file (by default, “bestroutes DATE TIME.csv”) each row of which represents a single itinerary:
Column 1: The net fuel cost (total fuel spend minus the value of fuel brought home (if “Always return home with an empty tank” is selected, this is equal to column 3)
Column 2: The value of fuel brought back to the home airport (if “Always return home with an empty tank” is selected, this is zero)
Column 3: The total cost of any extra stopovers
Column 4: The total fuel spend
Column 5: The IATA code of the home airport
Column 6: The amount of fuel to buy at the home airport
This is followed by two columns for each additional fuels stop: a column with the IATA code and a column with the amount of fuel to buy at that airport.
Where a route cannot be completed or another error occurs (such as an error in one of the rows of the input file) it is noted in the output file.

