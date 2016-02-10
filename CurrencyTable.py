import csv
from Currency import Currency


class CountryCurrencyFileError(Exception):
    pass


class ExchangeRateFileError(Exception):
    pass


class CurrencyTable:
    """
    CurrencyTable: holds information about countries, their currencies and exchange rates.
    The information is stored in a dictionary, the key to which is the country name.

    Input: two csv files.

    The first csv file has the following required columns:
    Column 1:  Country name.
    Column 15: Currency code.

    The second csv file has the following required columns:
    Column 2:  Currency code.
    Column 3:  Euro buy rate.

    The class raises two custom errors, CountryCurrencyFileError and ExchangeRateFileError,
    so that the main program can inform the user which file caused a FileNotFoundError.

    The class has one mutator method, __build_currency_table(), and one accessor method,
    get_exchange_rate(country).
    """

    def __init__(self, currency_file='input files/countrycurrency.csv',
                 exchange_rate_file='input files/currencyrates.csv',
                 real_exch_rates=True):
        self.__dictionary = self.__build_currency_table(currency_file, exchange_rate_file)
        self.__real_time_exchange_rates = real_exch_rates

    def __build_currency_table(self, currency_file, exchange_rate_file):
        dictionary = {}                                 # a temporary variable to store the contents of the first file

        # read countries and currencies from file
        try:
            with open(currency_file, 'rt') as f:
                reader = list(csv.reader(f))
        except FileNotFoundError:
            raise CountryCurrencyFileError
        else:
            for row in reader:
                key = row[0]
                if key != "name":                                                 # don't include header in dictionary
                    dictionary[key] = [row[0], row[14]]

        # read exchange rates from file and return a dictionary
        try:
            with open(exchange_rate_file, 'rt') as f:
                reader = list(csv.reader(f))
        except FileNotFoundError:
            raise ExchangeRateFileError
        else:
            output = {}
            for key in dictionary:
                for row in reader:
                    if row[1] == dictionary[key][1]:
                        output[key] = Currency(dictionary[key][0], row[0], dictionary[key][1], row[2])
        return output

    def get_exchange_rate(self, country):
        """
        Returns the real-time exchange rate if self.__real_time_exchange_rates is True.
        Otherwise returns the exchange rate from the file.
        """
        if self.__real_time_exchange_rates:
            return self.__dictionary[country].get_real_time_rate()
        else:
            return self.__dictionary[country].get_exchange_rate()


def main():
    currency_table = CurrencyTable()
    print(currency_table.get_exchange_rate("Afghanistan"))

if __name__ == '__main__':
    main()
