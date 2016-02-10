import urllib.request
from urllib.error import URLError
URL = "https://www.google.com/finance/converter?a=1&from="
START = "<span class=bld>"
END = " "

class Currency:
    """
    Currency class: holds information about a country, its currency and the euro exchange rate.
    It contains an accessor method, get_exchange_rate(), and two mutator methods,
    __find_real_time_sell_rate() and __find_real_time_exchange_rate().
    get_real_time_rate() is both an accessor and a mutator method.
    """

    def __init__(self, country_name, currency_name, currency_code, buy_rate):
        self.__country_name = country_name
        self.__currency_name = currency_name
        self.__currency_code = currency_code
        self.__exchange_rate = float(buy_rate)
        self.__real_time_rate = None

    def get_exchange_rate(self):
        """ Returns the exchange rate that was input from the csv file. """
        return self.__exchange_rate

    def get_real_time_rate(self):
        """
        Checks if the object contains real-time exchange rate.
        If not, gets the real-time exchange rate from internet and saves it to self.__real_time_rate.
        Then returns the real-time exchange rate.
        """
        if self.__real_time_rate == 0.0:
            # if the object previously failed to download real-time rate, it won't try again
            return self.__exchange_rate
        elif self.__real_time_rate is not None:
            # if real-time rate has already been stored, return it
            return self.__real_time_rate
        else:
            # attempt to get real-time exchange rate from the internet
            real_time_rate = self.__find_real_time_exchange_rate()
            self.__real_time_rate = real_time_rate
            if real_time_rate == 0.0:
                # if attempt to get real-time rate fails, return the exchange rate from the file
                return self.__exchange_rate
            else:
                return self.__real_time_rate

    def __find_real_time_sell_rate(self):
        """ Saves and returns the sell rate between self.__currency_code and euros """
        code = self.__currency_code
        url = URL + "EUR&to=" + code
        try:
            with urllib.request.urlopen(url) as f:
                page = str(f.read())
        except URLError:
            # if unable to connect to the website
            print("Unable to get real-time exchange rate for ", self.__country_name,
                  ". Using exchange rate from file", sep="")
            return 0.0

        # find the exchange rate within the page content
        start_of_exchange_rate = page.find(START) + 16
        end_of_exchange_rate = page.find(END, start_of_exchange_rate)

        # if web page doesn't contain the expected content
        if start_of_exchange_rate == 15 or end_of_exchange_rate == -1:
            print("Unable to get real-time exchange rate for ", self.__country_name,
                  ". Using exchange rate from file", sep="")
            return 0.0

        else:
            sell_rate = page[start_of_exchange_rate:end_of_exchange_rate]
        return float(sell_rate)

    def __find_real_time_exchange_rate(self):
        """ Returns the buy rate betweeen self.__currency_code and euros """
        code = self.__currency_code

        # deal with exceptional currencies first
        if code == "EUR":
            return 1
        elif code == "ZWD":
            code = "ZWL"                                                  # "ZWD" code no longer in use
        elif code in ["BYR", "IRR", "STD", "VND"]:                        # Google Finance doesn't have these buy rates
            sell_rate = self.__find_real_time_sell_rate()
            if sell_rate == 0.0:
                print("Failed to convert from", code, "to euro")
                return 0.0
            else:
                # return the reciprocal of the sell rate
                return 1 / sell_rate

        url = URL + code + "&to=EUR"
        try:
            with urllib.request.urlopen(url) as f:
                page = str(f.read())
        except URLError:
            # if unable to connect to the website
            print("Unable to get real-time exchange rate for ", self.__country_name,
                  ". Using exchange rate from file", sep="")
            return 0.0

        # find the exchange rate within the page content
        start_of_exchange_rate = page.find(START) + 16
        end_of_exchange_rate = page.find(END, start_of_exchange_rate)

        # if web page doesn't contain the expected content
        if start_of_exchange_rate == 15 or end_of_exchange_rate == -1:
            # try getting the sell rate instead
            sell_rate = self.__find_real_time_sell_rate()
            if sell_rate == 0.0:
                print("Failed to convert from", code, "to euro")
                return None
            else:
                # return the reciprocal of the sell rate
                return 1 / sell_rate
        else:
            exchange_rate = page[start_of_exchange_rate:end_of_exchange_rate]
        return float(exchange_rate)

    def __str__(self):
        output = "The currency of " + str(self.__country_name) + " is the " + str(self.__currency_name) + " (" + \
                 str(self.__currency_code) + ").  According to the file, the exchange rate is: " \
                 + str(self.__exchange_rate)
        if self.__real_time_rate != 0:
            output += ".\nToday's exchange rate is " + str(self.__real_time_rate)
        return output


def main():
    print()
    my_currency = Currency("Ireland", "punt", "IEP", 1.2697)
    my_currency.get_real_time_rate()
    print(my_currency)

if __name__ == '__main__':
    main()
