#! python3
from main import manage_list_of_routes, manage_single_route
from tkinter import Tk, Frame, BOTH, RAISED, Button, Checkbutton, BooleanVar, filedialog, END, Label, LabelFrame, Entry
from validate_inputs import validate_inputs_for_single_itinerary, validate_inputs_for_list_of_itineraries

class GraphicalUserInterface(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.__initUI()

    def __initUI(self):
        self.parent.title("Fuel Manager")

        # parameters that the user can modify
        self.__exchvar = BooleanVar()
        self.__exchrate = True
        self.__datevar = BooleanVar()
        self.__datetime = True
        self.__empty_tank_var = BooleanVar()
        self.__empty_tank = False
        self.__airport_file = "input files/airport.csv"
        self.__aircraft_file = "input files/aircraft.csv"
        self.__currency_file = "input files/countrycurrency.csv"
        self.__exchange_rate_file = "input files/currencyrates.csv"
        self.__itinerary_file = "input files/testroutes.csv"
        self.__output_file = "bestroutes/bestroutes.csv"
        self.__home_airport = ["DUB"]
        self.__other_airports = ["LHR", "CDG", "JFK", "AAL", "AMS", "ORK"]
        self.__hubs = ["MHP"]
        self.__stopover_cost = 0
        self.__constraints = "JFK AAL / JFK CDG"
        self.__aircraft_code = "747"

        # main frame
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        # manage single itinerary frame
        self.manual_frame = LabelFrame(self, text="Manage a single itinerary", font=("Helvetica", 14), width=300)
        self.manual_frame.place(x=50, y=50)

        # Empty row to put some space between the other rows and to control the width of this frame because
        # I don't know what I'm doing
        self.empty_label = Label(self.manual_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=0, sticky="W")

        # Text field where user can enter home airport
        self.home_airport_label = Label(self.manual_frame, width=22, text="Home airport:", anchor='w')
        self.home_airport_label.grid(row=1, sticky="W")
        self.home_airport_entry = Entry(self.manual_frame, width=50)
        self.home_airport_entry.grid(row=2, sticky="E")
        self.home_airport_entry.insert(0, self.__home_airport)

        self.empty_label = Label(self.manual_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=3, sticky="W")

        # Text field where user can enter other airports
        self.other_airports_label = Label(self.manual_frame, width=22, text="Other airports:", anchor='w')
        self.other_airports_label.grid(row=4, sticky="W")
        self.other_airports_entry = Entry(self.manual_frame, width=50)
        self.other_airports_entry.grid(row=5, sticky="E")
        self.other_airports_entry.insert(0, self.__other_airports)

        self.empty_label = Label(self.manual_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=6, sticky="W")

        # Text field where user can enter aircraft code
        self.aircraft_label = Label(self.manual_frame, width=22, text="Aircraft code:", anchor='w')
        self.aircraft_label.grid(row=7, sticky="W")
        self.aircraft_entry = Entry(self.manual_frame, width=50)
        self.aircraft_entry.grid(row=8, sticky="E")
        self.aircraft_entry.insert(0, self.__aircraft_code)

        self.empty_label = Label(self.manual_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=9, sticky="W")

        # Text field where user can enter constraints
        self.constraints_label = Label(self.manual_frame, width=22, text="Constraints:", anchor='w')
        self.constraints_label.grid(row=13, sticky="W")
        self.constraints_entry = Entry(self.manual_frame, width=50)
        self.constraints_entry.grid(row=14, sticky="E")
        self.constraints_entry.insert(0, self.__constraints)
        self.constraints_explanation_label = \
            Label(self.manual_frame, width=50,
                  text="Each constraint should consist of three-letter airport codes"
                       "\nseparated by spaces. To enter more than one constraint,"
                       "\nuse ' / ' to separate them", anchor='w', justify='left')
        self.constraints_explanation_label.grid(row=15, sticky="W")

        self.empty_label = Label(self.manual_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=16, sticky="W")

        # run button
        self.run_button = Button(self.manual_frame, text='Manage itinerary', command=self.__manage_single_itinerary,
                                 bg="#CCE1E8")
        self.run_button.grid(row=16, sticky="E")

        # manage list of itineraries frame
        self.itinerary_list_frame = LabelFrame(self, text="Manage a list of itineraries",
                                               font=("Helvetica", 14), width=300)
        self.itinerary_list_frame.place(x=50, y=375)

        # Empty row to put some space between the other rows and to control the width of this frame
        self.empty_label = Label(self.itinerary_list_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=12, sticky="W")

        # Text field where user can enter itinerary filepath
        self.itinerary_label = Label(self.itinerary_list_frame, width=22, text="Itinerary list: ", anchor='w')
        self.itinerary_label.grid(row=13, sticky="W")
        self.itinerary_entry = Entry(self.itinerary_list_frame, width=50)
        self.itinerary_entry.grid(row=13, sticky="E")
        self.itinerary_entry.insert(0, self.__itinerary_file)
        self.itinerary_button = Button(self.itinerary_list_frame, text='Browse...',
                                       command=self.__get_itinerary_filename)
        self.itinerary_button.grid(row=14, sticky="E")

        self.empty_label = Label(self.itinerary_list_frame, text=" ", width=60, height=2, font=("Helvetica", 1))
        self.empty_label.grid(row=15, sticky="W")

        # run button
        self.run_button = Button(self.itinerary_list_frame, text='Manage list of itineraries',
                                 command=self.__manage_list, bg="#CCE1E8")
        self.run_button.grid(row=16, sticky="E")

        # Fuel management settings frame
        self.general_frame = LabelFrame(self, text="Fuel management settings", font=("Helvetica", 14), width=300)
        self.general_frame.place(x=500, y=50)

        # Empty row to put some space between the other rows and to control the width of this frame
        self.empty_label = Label(self.general_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=0, sticky="W")

        # Text field where user can enter hubs
        self.hubs_label = Label(self.general_frame, width=22, text="Hubs:", anchor='w')
        self.hubs_label.grid(row=1, sticky="W")
        self.hubs_entry = Entry(self.general_frame, width=50)
        self.hubs_entry.grid(row=2, sticky="E")
        self.hubs_entry.insert(0, self.__hubs)

        self.empty_label = Label(self.general_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=3, sticky="W")

        # Text field where user can enter cost of extra stopovers
        self.stopover_cost_label = Label(self.general_frame, width=40, text="Cost of each extra stopover (euros):",
                                         anchor='w')
        self.stopover_cost_label.grid(row=4, sticky="W")
        self.stopover_cost_entry = Entry(self.general_frame, width=50)
        self.stopover_cost_entry.grid(row=5, sticky="E")
        self.stopover_cost_entry.insert(0, self.__stopover_cost)

        self.empty_label = Label(self.general_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=6, sticky="W")

        # bring home extra fuel checkbox
        self.empty_tank_cb = Checkbutton(self.general_frame,
                                         text="Always return to home airport with an empty tank",
                                         variable=self.__empty_tank_var, command=self.__empty_tank_toggle)
        self.empty_tank_cb.grid(row=7, sticky="W")

        self.empty_label = Label(self.general_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=8, sticky="W")

        # manage inputs frame
        self.input_frame = LabelFrame(self, text="Inputs", font=("Helvetica", 14), width=300)
        self.input_frame.place(x=500, y=250)

        self.empty_label = Label(self.input_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=0, sticky="W")

        # Text field where user can enter airport filepath
        self.airport_label = Label(self.input_frame, width=22, text="Airport list: ", anchor='w')
        self.airport_label.grid(row=1, sticky="W")
        self.airport_entry = Entry(self.input_frame, width=50)
        self.airport_entry.grid(row=1, sticky="E")
        self.airport_entry.insert(0, self.__airport_file)
        self.airport_button = Button(self.input_frame, text='Browse...', command=self.__get_airport_filename)
        self.airport_button.grid(row=2, sticky="E")

        self.empty_label = Label(self.input_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=3, sticky="W")

        # Text field where user can enter aircraft filepath
        self.aircraft_file_label = Label(self.input_frame, width=22, text="Aircraft list: ", anchor='w')
        self.aircraft_file_label.grid(row=4, sticky="W")
        self.aircraft_file_entry = Entry(self.input_frame, width=50)
        self.aircraft_file_entry.grid(row=4, sticky="E")
        self.aircraft_file_entry.insert(0, self.__aircraft_file)
        self.aircraft_file_button = Button(self.input_frame, text='Browse...', command=self.__get_aircraft_filename)
        self.aircraft_file_button.grid(row=5, sticky="E")

        self.empty_label = Label(self.input_frame, text=" ", width=425, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=6, sticky="W")

        # Text field where user can enter country-currency filepath
        self.currency_label = Label(self.input_frame, width=22, text="Currency list: ", anchor='w')
        self.currency_label.grid(row=7, sticky="W")
        self.currency_entry = Entry(self.input_frame, width=50)
        self.currency_entry.grid(row=7, sticky="E")
        self.currency_entry.insert(0, self.__currency_file)
        self.currency_button = Button(self.input_frame, text='Browse...', command=self.__get_currency_filename)
        self.currency_button.grid(row=8, sticky="E")

        self.empty_label = Label(self.input_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=9, sticky="W")

        # Text field where user can enter exchange rate filepath
        self.exchange_rate_label = Label(self.input_frame, width=22, text="Exchange rate list: ", anchor='w')
        self.exchange_rate_label.grid(row=10, sticky="W")
        self.exchange_rate_entry = Entry(self.input_frame, width=50)
        self.exchange_rate_entry.grid(row=10, sticky="E")
        self.exchange_rate_entry.insert(0, self.__exchange_rate_file)
        self.exchange_rate_button = Button(self.input_frame, text='Browse...', command=self.__get_exchange_rate_filename)
        self.exchange_rate_button.grid(row=11, sticky="E")

        # real-time exchange rates checkbox
        self.forex = Checkbutton(self.input_frame, text="Use real-time exchange rates", variable=self.__exchvar,
                                 command=self.__forex_toggle)
        self.forex.select()
        self.forex.grid(row=12, sticky="W")

        # manage output frame
        self.output_frame = LabelFrame(self, text="Output", font=("Helvetica", 14), width=300)
        self.output_frame.place(x=500, y=550)

        self.empty_label = Label(self.output_frame, text=" ", width=60, height=1, font=("Helvetica", 1))
        self.empty_label.grid(row=0, sticky="W")

        # Text field where user can enter output filepath
        self.output_label = Label(self.output_frame, width=22, text="Output file: ", anchor='w')
        self.output_label.grid(row=1, sticky="W")
        self.output_entry = Entry(self.output_frame, width=50)
        self.output_entry.grid(row=1, sticky="E")
        self.output_entry.insert(0, self.__output_file)
        self.output_button = Button(self.output_frame, text='Browse...', command=self.__get_output_filename)
        self.output_button.grid(row=2, sticky="E")

        # append date to output filename checkbox
        self.datetime_cb = Checkbutton(self.output_frame,
                                       text="Append date and time to filename (e.g., bestroutes 20151218 160000.csv)",
                                       variable=self.__datevar, command=self.__datetime_toggle)
        self.datetime_cb.grid(row=3, sticky="W")
        self.datetime_cb.select()

    # GUI methods

    def __forex_toggle(self):
        if self.__exchvar.get() == True:
            self.__exchrate = True
        else:
            self.__exchrate = False

    def __datetime_toggle(self):
        if self.__datevar.get() == True:
            self.__datetime = True
        else:
            self.__datetime = False

    def __empty_tank_toggle(self):
        if self.__empty_tank_var.get() == True:
            self.__empty_tank = True
        else:
            self.__empty_tank = False

    def __get_airport_filename(self):
        self.__airport_file = filedialog.askopenfilename(
            filetypes=(("Comma-separated values files", "*.csv"), ("All files", "*.*")))
        self.airport_entry.delete(0, END)
        self.airport_entry.insert(0, self.__airport_file)

    def __get_aircraft_filename(self):
        self.__aircraft_file = filedialog.askopenfilename(
            filetypes=(("Comma-separated values files", "*.csv"), ("All files", "*.*")))
        self.aircraft_file_entry.delete(0, END)
        self.aircraft_file_entry.insert(0, self.__aircraft_file)

    def __get_currency_filename(self):
        self.__currency_file = filedialog.askopenfilename(
            filetypes=(("Comma-separated values files", "*.csv"), ("All files", "*.*")))
        self.currency_entry.delete(0, END)
        self.currency_entry.insert(0, self.__currency_file)

    def __get_exchange_rate_filename(self):
        self.__exchange_rate_file = filedialog.askopenfilename(
            filetypes=(("Comma-separated values files", "*.csv"), ("All files", "*.*")))
        self.exchange_rate_entry.delete(0, END)
        self.exchange_rate_entry.insert(0, self.__exchange_rate_file)

    def __get_itinerary_filename(self):
        self.__itinerary_file = filedialog.askopenfilename(
            filetypes=(("Comma-separated values files", "*.csv"), ("All files", "*.*")))
        self.itinerary_entry.delete(0, END)
        self.itinerary_entry.insert(0, self.__itinerary_file)

    def __get_output_filename(self):
        self.__output_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=(
            ("Comma-separated values file", "*.csv"), ("All Files", "*.*")))
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, self.__output_file)

    def __manage_list(self):
        # validate user inputs
        hubs, stopover_cost = validate_inputs_for_list_of_itineraries(self.hubs_entry.get().upper().split(),
                                                                      self.stopover_cost_entry.get())
        print("Managing list of itineraries...")
        manage_list_of_routes(self.__exchrate,
                      self.__datetime,
                      self.__empty_tank,
                      hubs,
                      stopover_cost,
                      self.itinerary_entry.get(),
                      self.airport_entry.get(),
                      self.aircraft_file_entry.get(),
                      self.currency_entry.get(),
                      self.exchange_rate_entry.get(),
                      self.output_entry.get())

    def __manage_single_itinerary(self):
        # validate user inputs
        try:
            hubs, stopover_cost, constraints_list, home_airport, other_airports, aircraft_code = \
                validate_inputs_for_single_itinerary(self.hubs_entry.get().upper().split(),
                                self.stopover_cost_entry.get(),
                                self.constraints_entry.get().upper().split(),
                                self.home_airport_entry.get().upper(),
                                self.other_airports_entry.get().upper().split(),
                                self.aircraft_entry.get().upper())
        except TypeError:
            return

        print("Managing single itinerary...")
        manage_single_route(home_airport,
                            other_airports,
                            aircraft_code,
                            self.__exchrate,
                            self.__datetime,
                            self.__empty_tank,
                            hubs,
                            stopover_cost,
                            constraints_list,
                            self.airport_entry.get(),
                            self.aircraft_file_entry.get(),
                            self.currency_entry.get(),
                            self.exchange_rate_entry.get(),
                            self.output_entry.get())


def main():
    root = Tk()
    root.geometry("1000x700+50+50")
    root.iconbitmap('plane.ico')
    GraphicalUserInterface(root)
    root.mainloop()

if __name__ == '__main__':
    main()
