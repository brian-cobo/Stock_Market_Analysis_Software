
# Brian Cobo
# Stock Visualization

# Library Imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import json
import matplotlib.dates as ates
import warnings
warnings.filterwarnings('ignore')

# File Imports
from APIData import get_API_key


class Stock:
    def __init__(self, symbol, stockInfo=None,
                 api_key = get_API_key(),
                 type_of_graph = None,
                 output_data_type = 'csv',
                 interval_in_minutes = 5,
                 output_size = 'full'):
        self.api_key = api_key
        self.symbol = symbol
        self.stockInfo = stockInfo
        self.type_of_graph = type_of_graph
        self.output_data_type = output_data_type
        self.interval_in_minutes = interval_in_minutes
        self.output_size = output_size

    def get_three_month_data(self):
        self.type_of_graph = 'TIME_SERIES_DAILY'
        three_month_URL = f'https://www.alphavantage.co/query?' \
              f'function={self.type_of_graph}&' \
              f'symbol={self.symbol}&' \
              f'apikey={self.api_key}'
        print(three_month_URL)
        return three_month_URL

    def get_three_month_csv_data(self):
        self.type_of_graph = 'TIME_SERIES_DAILY'
        three_month_csv = f'https://www.alphavantage.co/query?' \
                      f'function={self.type_of_graph}&' \
                      f'symbol={self.symbol}&' \
                      f'apikey={self.api_key}&' \
                      f'datatype={self.output_data_type}'
        print(three_month_csv)

    def get_intraday_data(self):
        self.type_of_graph = 'TIME_SERIES_INTRADAY'
        intraday_URL = f'https://www.alphavantage.co/query?' \
                       f'function={self.type_of_graph}&' \
                       f'symbol={self.symbol}&' \
                       f'interval={self.interval_in_minutes}min&' \
                       f'outputsize={self.output_size}&' \
                       f'apikey={self.api_key}'
        print(intraday_URL)
        return intraday_URL

    def get_intraday_csv_data(self):
        self.type_of_graph = 'TIME_SERIES_INTRADAY'
        intraday_CSV = f'https://www.alphavantage.co/query?' \
                       f'function={self.type_of_graph}&' \
                       f'symbol={self.symbol}&' \
                       f'interval={self.interval_in_minutes}min&' \
                       f'apikey={self.api_key}&' \
                       f'outputsize={self.output_size}&' \
                       f'datatype={self.output_data_type}'
        print(intraday_CSV)

    def get_daily_adjusted_data(self):
        self.type_of_graph = 'TIME_SERIES_DAILY'
        daily_adjusted_URL = 'https://www.alphavantage.co/query?' \
                             f'function={self.type_of_graph}&' \
                             f'symbol={self.symbol}&' \
                             f'apikey={self.api_key}'
                             #f'outputsize={self.output_size}&' \

        print(daily_adjusted_URL)
        return daily_adjusted_URL

    def print_current_stock_data(self):
        self.type_of_graph = 'GLOBAL_QUOTE'
        current_stock_data_URL = 'https://www.alphavantage.co/query?' \
                                 f'function={self.type_of_graph}&' \
                                 f'symbol={self.symbol}&' \
                                 f'apikey={self.api_key}'
        print(current_stock_data_URL)

        json_data = self.convert_url_data_into_json(current_stock_data_URL)
        stockInfo = pd.DataFrame(json_data)['Global Quote']
        print(stockInfo)



        return current_stock_data_URL

    def convert_url_data_into_json(self, url_data, print_data = False):
        with urllib.request.urlopen(url_data) as response:
            html = response.read()
            data = json.loads(html)

        if print_data:
            print(json.dumps(data, indent=4, sort_keys=True))

        return data

    def convert_json_to_dataframe(self, json_data, df_head = False,
                                  df_shape = False, df_columns = False,
                                  df_info = False):
        if self.type_of_graph == 'TIME_SERIES_INTRADAY':
            stockInfo = pd.DataFrame(json_data[f'Time Series ({self.interval_in_minutes}min)'])
        elif self.type_of_graph == 'TIME_SERIES_DAILY':
            stockInfo = pd.DataFrame(json_data['Time Series (Daily)'])
        else:
            print(f'ERROR: {self.type_of_graph} NOT RECOGNIZED BY PROGRAM')

        # Transposing data so that the rows and columns are flipped
        stockInfo = stockInfo.transpose()

        stockInfo = stockInfo.rename(columns={'1. open': 'Open',
                                              '2. high': 'High',
                                              '3. low': 'Low',
                                              '4. close': 'Close',
                                              '5. volume': 'Volume'})
        stockInfo['Date'] = stockInfo.index
        stockInfo.sort_values(by=['Date'], inplace=True)

        # Converting data columns to correct datatype
        stockInfo.Open = pd.to_numeric(stockInfo.Open)
        stockInfo.High = pd.to_numeric(stockInfo.High)
        stockInfo.Low = pd.to_numeric(stockInfo.Low)
        stockInfo.Close = pd.to_numeric(stockInfo.Close)
        stockInfo.Volume = pd.to_numeric(stockInfo.Volume)
        stockInfo.Date = pd.to_datetime(stockInfo.Date)

        if df_head:
            print('Data Head:')
            print(stockInfo.head(), '\n\n')

        if df_shape:
            print('Data Shape: (Rows, Columns)')
            print(stockInfo.shape, '\n\n')

        if df_columns:
            print('Data Columns:')
            print(stockInfo.columns, '\n\n')

        if df_info:
            print('Data Info:')
            print(stockInfo.info(), '\n\n')

        self.stockInfo = stockInfo
        return stockInfo

    def print_stockInfo_most_recent_10_days(self):
        print(self.stockInfo[-10:])

    def draw_graph(self, Close=True, Open=False,
                   High=False, Low=False, graph_width=12,
                   graph_height=8):
        stockInfo = self.stockInfo

        plt.figure(figsize=(graph_width, graph_height))
        ax = plt.subplot()

        if Close:
            plt.plot(stockInfo.Date, stockInfo.Close, label='Close Price', color='blue')

        if Open:
            plt.plot(stockInfo.Date, stockInfo.Open, label = 'Open Price', color = 'green')
        if High:
            plt.plot(stockInfo.Date, stockInfo.High, label = 'High', color = 'red')
        if Low:
            plt.plot(stockInfo.Date, stockInfo.Low, label = 'Low', color = 'orange')

        plt.title(self.symbol)
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.locator_params(axis='x', numticks=3)
        plt.legend()
        plt.gcf().autofmt_xdate()
        ax.xaxis.set_major_formatter(ates.DateFormatter('%b %d'))
        plt.show()

    def calculate_stochastic_oscillator(self):
        # The equation to calculate the stochastic oscillator is:

        # %K = 100(C – L14)/(H14 – L14)
        # Where:
        # C = the most recent closing price
        # L14 = the low of the 14 previous trading sessions
        # H14 = the highest price traded during the same 14-day period
        # %K= the current market rate for the currency pair
        # %D = 3-period moving average of %K

        # Create the "L14" column in the DataFrame
        self.stockInfo['L14'] = self.stockInfo['Low'].rolling(window=14).min()
        # Create the "H14" column in the DataFrame
        self.stockInfo['H14'] = self.stockInfo['High'].rolling(window=14).max()
        # Create the "%K" column in the DataFrame
        self.stockInfo['%K'] = 100 * ((self.stockInfo['Close'] - self.stockInfo['L14']) / (self.stockInfo['H14'] - self.stockInfo['L14']))
        # Create the "%D" column in the DataFrame
        self.stockInfo['%D'] = self.stockInfo['%K'].rolling(window=3).mean()

    def draw_stochastic_oscillator(self):
        self.calculate_stochastic_oscillator()
        fig, axes = plt.subplots(figsize=(20, 10))
        # self.stockInfo['Close'].plot(ax=axes[0]);
        # axes[0].set_title(self.symbol + ' Close Prices')
        self.stockInfo[['%K', '%D']].plot(ax=axes)
        axes.set_title(self.symbol + ' Stochastic Oscillator')
        plt.hlines(80, 0, 100, linestyles='dashed', color='red', data=self.stockInfo.Date)
        plt.hlines(20, 0, 100, linestyles='dashed', color='red', data=self.stockInfo.Date)
        plt.hlines(50, 0, 100, linestyles='dashed', color='black', data=self.stockInfo.Date)
        plt.show()

    def calculate_long_or_short(self):
        self.stockInfo['Sell Entry'] = ((self.stockInfo['%K'] < self.stockInfo['%D']) & (
                self.stockInfo['%K'].shift(1) > self.stockInfo['%D'].shift(1))) & (self.stockInfo['%D'] > 80)
        self.stockInfo['Sell Exit'] = (
                (self.stockInfo['%K'] > self.stockInfo['%D']) & (
                    self.stockInfo['%K'].shift(1) < self.stockInfo['%D'].shift(1)))
        self.stockInfo['Short'] = np.nan
        self.stockInfo.loc[self.stockInfo['Sell Entry'], 'Short'] = -1
        self.stockInfo.loc[self.stockInfo['Sell Exit'], 'Short'] = 0
        self.stockInfo['Short'][0] = 0
        self.stockInfo['Short'] = self.stockInfo['Short'].fillna(method='pad')
        self.stockInfo['Buy Entry'] = ((self.stockInfo['%K'] > self.stockInfo['%D']) & (
                self.stockInfo['%K'].shift(1) < self.stockInfo['%D'].shift(1))) & (self.stockInfo['%D'] < 20)
        self.stockInfo['Buy Exit'] = (
                (self.stockInfo['%K'] < self.stockInfo['%D']) & (
                    self.stockInfo['%K'].shift(1) > self.stockInfo['%D'].shift(1)))
        self.stockInfo['Long'] = np.nan
        self.stockInfo.loc[self.stockInfo['Buy Entry'], 'Long'] = 1
        self.stockInfo.loc[self.stockInfo['Buy Exit'], 'Long'] = 0
        self.stockInfo['Long'][0] = 0
        self.stockInfo['Long'] = self.stockInfo['Long'].fillna(method='pad')

        # Add Long and Short positions together to get final strategy position (1 for long, -1 for short and 0 for flat)
        self.stockInfo['Position'] = self.stockInfo['Long'] + self.stockInfo['Short']

        long_or_short = self.stockInfo.Position[-1]
        print(long_or_short)
        if long_or_short == -1:
            print('SHORT', self.symbol)
        if long_or_short == 0:
            print('HOLD', self.symbol)
        if long_or_short == 1:
            print('LONG', self.symbol)

        return long_or_short

    def draw_long_or_short_graph(self):
        self.calculate_long_or_short()
        self.stockInfo['Position'].plot(figsize=(20, 10))
        plt.xlabel('Date')
        plt.ylabel('-1 Short 1 Long')
        plt.show()


if __name__ == "__main__":
    choice = 0

    while choice != -1:
        choice = int(input('\n\nChoose Option:\n1: Get Historical Data\n2: Get Current Data\n-1: Quit\n'))
        stockSymbol = input("Enter a Stock to look at: ")
        stockSymbol = stockSymbol.upper()

        if choice == 1:
            stock = Stock(symbol=stockSymbol)
            data = stock.get_daily_adjusted_data()
            data = stock.convert_url_data_into_json(url_data=data)
            stock.convert_json_to_dataframe(json_data=data)
            stock.draw_graph(Close=True,Open=True)
            stock.draw_stochastic_oscillator()
            stock.draw_long_or_short_graph()

        elif choice == 2:
            stock = Stock(symbol=stockSymbol)
            data = stock.print_current_stock_data()

        elif choice == -1:
            print("Goodbye")
            exit(0)

        else:
            print('Choice not recognized')