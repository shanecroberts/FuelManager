from tkinter import messagebox

def validate_inputs_for_single_itinerary(hubs, stopover_cost, constraints_list, home_airport, other_airports, aircraft_code):

    # verify that each hub is a potential airport code
    for i in hubs:
        if len(i) != 3:
            title = "Invalid airport code"
            message = "Invalid hub: " + str(i) + "\nAn airport code should have three characters"
            messagebox.showerror(title, message)
            return None
        elif not i.isalnum():
            title = "Invalid airport code"
            message = "Invalid hub: " + str(i) + "\nAn airport code should only contain letters and numbers"
            messagebox.showerror(title, message)
            return None

    # verify that stopover_cost is a number
    try:
        stopover_cost = float(stopover_cost)
    except TypeError:
        title = "Invalid amount"
        message = "Invalid stopover cost: " + str(stopover_cost) + "\nPlease enter a number"
        messagebox.showerror(title, message)
        return None

    # verify that each item in the constraints field is an airport code or separator
    for i in constraints_list:
        if (i != "/") and ((len(i) != 3) or (not i.isalnum())):
            title = "Invalid constraint"
            message = "Invalid constraint: " + str(i) + \
                      "\nEach constraint should consist of three-letter airport codes separated by spaces" \
                      "\nTo enter more than one constraint, use ' / ' to separate them"
            messagebox.showerror(title, message)
            return None

    # split constraints string into a list of lists, each list being one constraint
    list_of_constraints = []
    current_constraint = []
    for i in range(len(constraints_list)):
        if constraints_list[i] == "/":
            list_of_constraints.append(current_constraint)
            current_constraint = []
        elif i == len(constraints_list) - 1:
            current_constraint.append(constraints_list[i])
            list_of_constraints.append(current_constraint)
        else:
            current_constraint.append(constraints_list[i])

    # verify that each home airport is a potential airport code
    if len(home_airport) != 3:
        title = "Invalid airport code"
        message = "Invalid home airport: " + str(home_airport) + "\nAn airport code should have three characters"
        messagebox.showerror(title, message)
        return None
    elif not home_airport.isalnum():
        title = "Invalid airport code"
        message = "Invalid home airport: " + str(home_airport) + \
                  "\nAn airport code should only contain letters and numbers"
        messagebox.showerror(title, message)
        return None

    # verify that each non-home is a potential airport code
    for i in other_airports:
        if len(i) != 3:
            title = "Invalid airport code"
            message = "Invalid airport: " + str(i) + "\nAn airport code should have three characters"
            messagebox.showerror(title, message)
            return None
        elif not i.isalnum():
            title = "Invalid airport code"
            message = "Invalid airport code: " + str(i) + "\nAn airport code should only contain letters and numbers"
            messagebox.showerror(title, message)
            return None

    # verify that aircraft_code makes sense
    if not aircraft_code.isalnum():
        title = "Invalid aircraft code"
        message = "Invalid aircraft code: " + str(aircraft_code) + \
                  "\nAn aircraft code should contain only letters and numbers"
        messagebox.showerror(title, message)
        return None

    return hubs, stopover_cost, list_of_constraints, home_airport, other_airports, aircraft_code


def validate_inputs_for_list_of_itineraries(hubs, stopover_cost):

    # verify that each hub is a potential airport code
    for i in hubs:
        if len(i) != 3:
            title = "Invalid airport code"
            message = "Invalid hub: " + str(i) + "\nAn airport code should have three characters"
            messagebox.showerror(title, message)
            return None
        elif not i.isalnum():
            title = "Invalid airport code"
            message = "Invalid hub: " + str(i) + "\nAn airport code should only contain letters and numbers"
            messagebox.showerror(title, message)
            return None

    # verify that stopover_cost is a number
    try:
        stopover_cost = float(stopover_cost)
    except TypeError:
        title = "Invalid amount"
        message = "Invalid stopover cost: " + str(stopover_cost) + "\nPlease enter a number"
        messagebox.showerror(title, message)
        return None

    return hubs, stopover_cost
