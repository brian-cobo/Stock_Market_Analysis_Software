
# Brian Cobo
# Stock Visualization

# Library Imports
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import json
import matplotlib.dates as ates
import warnings
from pandas.io.json import json_normalize
warnings.filterwarnings('ignore')
import time

# File Imports
from APIData import get_API_key

# Code Sources
#    - Stochastic Oscillation
#       - https://pythonforfinance.net/2017/10/10/stochastic-oscillator-trading-strategy-backtest-in-python/

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

    def get_five_months_data(self):
        self.type_of_graph = 'TIME_SERIES_MONTHLY'
        print('Get Five Month:', self.type_of_graph)
        three_month_URL = (f'https://www.alphavantage.co/query?'
                          f'function={self.type_of_graph}&'
                          f'symbol={self.symbol}&'
                          f'apikey={self.api_key}')
        print(three_month_URL)
        return three_month_URL

    def get_five_months_csv_data(self):
        self.type_of_graph = 'TIME_SERIES_DAILY'
        three_month_csv = (f'https://www.alphavantage.co/query?'
                          f'function={self.type_of_graph}&'
                          f'symbol={self.symbol}&'
                          f'apikey={self.api_key}&'
                          f'datatype={self.output_data_type}')
        print('CSV DOWNLOAD LINK:', three_month_csv)

    def get_months_data(self):
        print('Type:', self.type_of_graph)

        self.type_of_graph = 'TIME_SERIES_MONTHLY'

        print('Type:', self.type_of_graph)
        three_month_URL = (f'https://www.alphavantage.co/query?'
                          f'function={self.type_of_graph}&'
                          f'symbol={self.symbol}&'
                          f'outputsize={self.output_size}&'
                          f'apikey={self.api_key}')
        print("URL", three_month_URL)
        return three_month_URL


    def get_months_csv_data(self):
        self.type_of_graph = 'TIME_SERIES_MONTHLY'
        three_month_csv = (f'https://www.alphavantage.co/query?'
                          f'function={self.type_of_graph}&'
                          f'symbol={self.symbol}&'
                          f'outputsize={self.output_size}&'
                          f'apikey={self.api_key}&'
                          f'datatype={self.output_data_type}')
        print('CSV DOWNLOAD LINK:', three_month_csv)

    def get_intraday_data(self):
        self.type_of_graph = 'TIME_SERIES_INTRADAY'
        intraday_URL = (f'https://www.alphavantage.co/query?'
                       f'function={self.type_of_graph}&'
                       f'symbol={self.symbol}&'
                       f'interval={self.interval_in_minutes}min&'
                       f'outputsize={self.output_size}&'
                       f'apikey={self.api_key}')
        print(intraday_URL)
        return intraday_URL

    def get_intraday_csv_data(self):
        self.type_of_graph = 'TIME_SERIES_INTRADAY'
        intraday_CSV = (f'https://www.alphavantage.co/query?'
                       f'function={self.type_of_graph}&'
                       f'symbol={self.symbol}&'
                       f'interval={self.interval_in_minutes}min&'
                       f'apikey={self.api_key}&'
                       f'outputsize={self.output_size}&'
                       f'datatype={self.output_data_type}')
        print('CSV DOWNLOAD LINK:', intraday_CSV)

    def get_daily_adjusted_data(self):
        self.type_of_graph = 'TIME_SERIES_DAILY'
        daily_adjusted_URL = ('https://www.alphavantage.co/query?'
                             f'function={self.type_of_graph}&'
                             f'symbol={self.symbol}&'
                             f'apikey={self.api_key}')
                             # f'outputsize={self.output_size}&')

        print(daily_adjusted_URL)
        return daily_adjusted_URL

    def get_csv_daily_adjusted_data(self):
        self.type_of_graph = 'TIME_SERIES_DAILY'
        daily_adjusted_URL = ('https://www.alphavantage.co/query?'
                             f'function={self.type_of_graph}&'
                             f'symbol={self.symbol}&'
                             f'apikey={self.api_key}&'
                             f'datatype={self.output_data_type}')
                             #f'outputsize={self.output_size}&' \

        print('CSV DOWNLOAD LINK:', daily_adjusted_URL)

    def get_all_available_data(self):
        self.type_of_graph = 'TIME_SERIES_MONTHLY'
        available_data_URL = (f'https://www.alphavantage.co/query?'
                             f'function={self.type_of_graph}&'
                             f'symbol={self.symbol}&'
                             f'apikey={self.api_key}&'
                             f'outputsize={self.output_size}')

        print(available_data_URL)
        return available_data_URL

    def get_csv_all_available_data(self):
        self.type_of_graph = 'TIME_SERIES_MONTHLY'
        available_data_URL = (f'https://www.alphavantage.co/query?'
                              f'function={self.type_of_graph}&'
                              f'symbol={self.symbol}&'
                              f'apikey={self.api_key}&'
                              f'outputsize={self.output_size}&'
                              f'datatype={self.output_data_type}')

        print('CSV DOWNLOAD LINK:', available_data_URL)

    def get_current_stock_data(self):
        self.type_of_graph = 'GLOBAL_QUOTE'
        current_stock_data_URL = ('https://www.alphavantage.co/query?'
                                 f'function={self.type_of_graph}&'
                                 f'symbol={self.symbol}&'
                                 f'apikey={self.api_key}')
        #print(current_stock_data_URL)

        json_data = self.convert_url_data_into_json(current_stock_data_URL)
        stockInfo = pd.DataFrame(json_data)['Global Quote']
        stockInfo = stockInfo.transpose()

        stockInfo = stockInfo.rename(index={'01. symbol':'Symbol',
                                            '02. open':'Open',
                                            '03. high':'High',
                                            '04. low':'Low',
                                            '05. price':'Price',
                                            '06. volume':'Volume',
                                            '07. latest trading day':'Latest Trading Day',
                                            '08. previous close':'Previous Close',
                                            '09. change':'Change',
                                            '10. change percent':'Change Percent'
                                             }
                                    )

        # Converting data columns to correct datatype
        stockInfo.Open = pd.to_numeric(stockInfo.Open)
        stockInfo.High = pd.to_numeric(stockInfo.High)
        stockInfo.Low = pd.to_numeric(stockInfo.Low)
        stockInfo.Price = pd.to_numeric(stockInfo.Price)
        stockInfo.Volume = pd.to_numeric(stockInfo.Volume)
        stockInfo.Change = pd.to_numeric(stockInfo.Change)
        stockInfo['Latest Trading Day'] = pd.to_datetime(stockInfo['Latest Trading Day'])
        stockInfo['Previous Close'] = pd.to_numeric(stockInfo['Previous Close'])

        return stockInfo

    def convert_url_data_into_json(self, url_data, print_data=False):
        with urllib.request.urlopen(url_data) as response:
            html = response.read()
            data = json.loads(html)

        if print_data:
            print(json.dumps(data, indent=4, sort_keys=True))

        return data

    def convert_json_to_dataframe(self, json_data, df_head=False,
                                  df_shape=False, df_columns=False,
                                  df_info=False):

        try:
            if self.type_of_graph == 'TIME_SERIES_INTRADAY':
                stockInfo = pd.DataFrame(json_data[f'Time Series ({self.interval_in_minutes}min)'])
            if self.type_of_graph == 'TIME_SERIES_DAILY':
                stockInfo = pd.DataFrame(json_data['Time Series (Daily)'])
            if self.type_of_graph == 'TIME_SERIES_MONTHLY':
                stockInfo = pd.DataFrame(json_data['Monthly Time Series'])
        except:
            raise Exception (f'ERROR: {self.type_of_graph} NOT RECOGNIZED BY PROGRAM')

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
        ax.xaxis.set_major_formatter(ates.DateFormatter('%b %d %y'))
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

def ask_for_stock_symbol():
    stockSymbol = input("\nEnter a Stock to look at: ")
    stockSymbol = stockSymbol.upper()
    return stockSymbol

def check_if_attribute_in_list(option, list):
    if option in list:
        return True
    else:
        return False

def get_historical_data(stockSymbol):
    data_range = int(input('Choose Data Option:\n'
                           '1: Five Months Data\n'
                           '2: Daily Adjusted Data\n'
                           '3: Intraday Data\n'
                           '4: All Available Data\n'))
    print_csv_link = int(input('Do you want the link to download csv files?\n'
                               '1: Yes\n'
                               '2: No\n'))
    draw_graphs = int(input('\nDo you want to draw graphs?\n'
                            '1: Yes\n'
                            '2: No\n'))

    stock = Stock(symbol=stockSymbol)

    if choice == 2:
        data = stock.get_daily_adjusted_data()
        if print_csv_link == 1:
            stock.get_csv_daily_adjusted_data()

    elif choice == 3:
        data = stock.get_intraday_data()
        if print_csv_link == 1:
            stock.get_intraday_csv_data()

    elif choice == 4:
        data = stock.get_all_available_data()
        if print_csv_link == 1:
            stock.get_csv_all_available_data()
    else:
        data = stock.get_five_months_data()
        if print_csv_link == 1:
            stock.get_five_months_csv_data()

    data = stock.convert_url_data_into_json(url_data=data)
    print(data)
    data = stock.convert_json_to_dataframe(json_data=data)
    print('\nFirst 10 entries:\n', data.head(10))
    print('\nLast 10 entries:\n', data.tail(10))



    if draw_graphs == 1:
        attributes = input("\nWhich attributes would you like to draw?"
                               "If multiple attributes, put a comma between them.\n"
                               "1: Close\n"
                               "2: Open\n"
                               "3: High\n"
                               "4: Low\n")
        attributes = attributes.split(',')
        attributes = (' ').join(attributes)

        stock.draw_graph(Close=check_if_attribute_in_list('1', attributes),
                         Open=check_if_attribute_in_list('2', attributes),
                         High=check_if_attribute_in_list('3', attributes),
                         Low=check_if_attribute_in_list('4', attributes))
        draw_stoch = int(input("\nWould you like to draw a stochastic oscillator?\n"
                               "1: Yes\n"
                               "2: No\n"))
        if draw_stoch != 2:
            stock.draw_stochastic_oscillator()

            draw_long_short = int(input("\nWould you like to draw the long or short graph based on the oscillator?\n"
                                        "1: Yes\n"
                                        "2: No\n"))
            if draw_long_short != 2:
                stock.draw_long_or_short_graph()


def get_current_data(stockSymbol, print_results=False):
    stock = Stock(symbol=stockSymbol)
    data = stock.get_current_stock_data()
    if print_results == True:
        print('\nData:', data)
    return data


def get_sector_data():
    sectorDataUrl = f'https://www.alphavantage.co/query?' \
                    f'function=SECTOR&' \
                    f'apikey={get_API_key()}'
    with urllib.request.urlopen(sectorDataUrl) as response:
        html = response.read()
        data = json.loads(html)

    sector = int(input('\nWhich Sector Data would you like to view?\n'
                       '0: Real-Time Performance\n'
                       '1: 1 Day Performance\n'
                       '2: 5 Day Performance\n'
                       '3: 1 Month Performance\n'
                       '4: 3 Month Performance\n'
                       '5: Year To Date Performance\n'
                       '6: 1 Year Performance\n'
                       '7: 3 Year Performance\n'
                       '8: 5 Year Performance\n'
                       '9: 10 Year Performance\n'))
    if sector == 1:
        data = json_normalize(data['Rank B: 1 Day Performance'], meta=['Sector', 'Change'])
    elif sector == 2:
        data = json_normalize(data['Rank C: 5 Day Performance'])
    elif sector == 3:
        data = json_normalize(data['Rank D: 1 Month Performance'])
    elif sector == 4:
        data = json_normalize(data['Rank E: 3 Month Performance'])
    elif sector == 5:
        data = json_normalize(data['Rank F: Year-to-Date (YTD) Performance'])
    elif sector == 6:
        data = json_normalize(data['Rank G: 1 Year Performance'])
    elif sector == 7:
        data = json_normalize(data['Rank H: 3 Year Performance'])
    elif sector == 8:
        data = json_normalize(data['Rank I: 5 Year Performance'])
    elif sector == 9:
        data = json_normalize(data['Rank J: 10 Year Performance'])
    else:
        data = json_normalize(data['Rank A: Real-Time Performance'])

    data = data.transpose()
    print(data)



def create_market_report():
    filePath = os.getcwd + '/Spreadsheets/Market_Summary.xlsx'
    nasdaq_data = pd.read_csv('Nasdaq_Company_List.csv')
    marketData = pd.DataFrame(columns=['Symbol', 'Name', 'Price', 'Change',
                                       'Change_Percent', 'Open', 'High', 'Low',
                                       'Previous_Close', 'Volume', 'Latest_Trading_Day',
                                       'Industry', 'Sector', 'Summary_Quote'])

    for i in range(len(nasdaq_data)):
        try:
            time.sleep(0.3)
            data = marketData
            data.Symbol = nasdaq_data['Symbol']
            data.Name = nasdaq_data['Name']
            data.Sector = nasdaq_data['Sector']
            data.Industry = nasdaq_data['Industry']
            data.Summary_Quote = nasdaq_data['Summary Quote']

            name = marketData.Symbol.iloc[i]
            currentData = get_current_data(name)

            data.iloc[i].Price = currentData['Price']
            data.iloc[i].Change = currentData['Change']
            data.iloc[i].Change_Percent = currentData['Change Percent']
            data.iloc[i].Open = currentData['Open']
            data.iloc[i].High = currentData['High']
            data.iloc[i].Low = currentData['Low']
            data.iloc[i].Previous_Close = currentData['Previous Close']
            data.iloc[i].Volume = currentData['Volume']
            data.iloc[i].Latest_Trading_Day = currentData['Latest Trading Day']
            marketData.append(data)

            if i % 50 == 0:
                print(f'{i} of {len(nasdaq_data)} Stocks')
                marketData.to_excel(filePath)

        except Exception as e:
            print(f'ERROR Grabbing Data for {name}:', e)


    marketData.to_excel(filePath)
    print("Market_Summary.xlsx has been created.")


def split_percentage(change):
    try:
        change = float(change.split('%')[0])
        return change

    except Exception as e:
        print(e)


def analyze_market_data():
    filePath = os.getcwd + '/Spreadsheets/Market_Summary.xlsx'
    market_summary = pd.read_excel(filePath)
    print(market_summary.info(),'\n\n\n\n')
    market_summary.Change_Percent = market_summary.Change_Percent.apply(lambda x: split_percentage(x))

    change = market_summary.Change_Percent[(type(market_summary.Change_Percent) !=float)]
    print(change)

def search_for_company_symbol(keyword_to_search_for, automated=False):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword_to_search_for}&apikey={get_API_key()}'
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read()
            data = json.loads(html)

        length_of_results = len(data['bestMatches'])
        data = json_normalize(data['bestMatches'])
        data = data.rename(columns = {'1. symbol' : 'Symbol',
                                      '2. name' : 'Name',
                                      '3. type' : 'Type',
                                      '4. region' : 'Region',
                                      '5. marketOpen' : 'Market_Open',
                                      '6. marketClose' : 'Market_Close',
                                      '7. timezone' : 'Timezone',
                                      '8. currency' : 'Currency',
                                      '9. matchScore' : 'Match_Score'})
        if automated == True:
            return data

        index = 0
        answer = 0
        while index < length_of_results or answer != 1:
            print('\nSymbol:', data.Symbol.iloc[index],
                  '\nName:', data.Name.iloc[index],
                  '\nMatch:', data.Match_Score.iloc[index])
            answer = int(input('Is this what you are looking for?\n'
                               '1: Yes\n'
                               '2: No\n'))
            if answer == 1:
                return data.Symbol.iloc[index]
            index += 1

        print('\nNo Stocks Found')
        return None

    except:
        return None



if __name__ == "__main__":
    choice = 0
    print('Welcome')
    while choice != -1:
        choice = int(input('\nChoose Option:\n'
                           '1: Get Historical Data\n'
                           '2: Get Current Data\n'
                           '3: Create Market Report\n'
                           '4: Get Sector Data\n'
                           '5: Search for Company Symbol\n'
                           '-1: Quit\n'))
        if choice == -1:
            print("\nGoodbye")

        elif choice == 1:
            stockSymbol = ask_for_stock_symbol()
            get_historical_data(stockSymbol)

        elif choice == 2:
            stockSymbol = ask_for_stock_symbol()
            get_current_data(stockSymbol, print_results=True)

        elif choice == 3:
            create_market_report()

        elif choice == 4:
            get_sector_data()

        elif choice == 5:
            keyword_to_search_for = input('\nWhat keyword would you like to search for? ')
            search_for_company_symbol(keyword_to_search_for)

        else:
            print('Choice not recognized')
