 
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
    def __init__(self, symbol,
                 api_key = get_API_key(),
                 type_of_graph = None,
                 output_data_type = 'csv',
                 interval_in_minutes = 5,
                 output_size = 'full'):
        self.api_key = api_key
        self.symbol = symbol
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
            stockInfo = pd.DataFrame(data[f'Time Series ({self.interval_in_minutes}min)'])
        elif self.type_of_graph == 'TIME_SERIES_DAILY':
            stockInfo = pd.DataFrame(data['Time Series (Daily)'])
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

        return stockInfo


levi = Stock(symbol='LEVI')
data = levi.get_intraday_data()
data = levi.convert_url_data_into_json(url_data=data, print_data=False)
data = levi.convert_json_to_dataframe(json_data=data, df_head=True,
                                      df_shape=True, df_columns =True,
                                      df_info=True)



plt.figure(figsize = (12, 8))
ax = plt.subplot()
plt.plot(stockInfo.Date, stockInfo.Close, label = 'Close Price', color = 'blue')
#plt.plot(stockInfo.Date, stockInfo.Open, label = 'Open Price', color = 'green')
#plt.plot(stockInfo.Date, stockInfo.High, label = 'High', color = 'red')
#plt.plot(stockInfo.Date, stockInfo.Low, label = 'Low', color = 'orange')
plt.title(symbol)
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.locator_params(axis='x', numticks=3)
plt.legend()
plt.gcf().autofmt_xdate()
ax.xaxis.set_major_formatter(ates.DateFormatter('%b %d'))
plt.show()
 
#Now that we have a basic graph drawn, I want to draw out a stochastic oscillator for the stock.
#A Stochastic Oscillator is a momentum indicator comparing a particular closing price of a security to a range of its prices over a certain period of time. The sensitivity of the oscillator to market movements is reducible by adjusting that time period or by taking a moving average of the result.
#The equation to calculate the stochastic oscillator is:

#%K = 100(C – L14)/(H14 – L14)
#Where:
#C = the most recent closing price
#L14 = the low of the 14 previous trading sessions
#H14 = the highest price traded during the same 14-day period
#%K= the current market rate for the currency pair
#%D = 3-period moving average of %K


#Create the "L14" column in the DataFrame
stockInfo['L14'] = stockInfo['Low'].rolling(window=14).min()
#Create the "H14" column in the DataFrame
stockInfo['H14'] = stockInfo['High'].rolling(window=14).max()
#Create the "%K" column in the DataFrame
stockInfo['%K'] = 100*((stockInfo['Close'] - stockInfo['L14']) / (stockInfo['H14'] - stockInfo['L14']) )
#Create the "%D" column in the DataFrame
stockInfo['%D'] = stockInfo['%K'].rolling(window=3).mean()

fig, axes = plt.subplots(nrows=2, ncols=1,figsize=(20,10))
stockInfo['Close'].plot(ax=axes[0]); axes[0].set_title(symbol + ' Close Prices')
stockInfo[['%K','%D']].plot(ax=axes[1]); axes[1].set_title(symbol + ' Stochastic Oscillator')
plt.hlines(80, 0, 100, linestyles = 'dashed', color = 'red', data = stockInfo.Date)
plt.hlines(20, 0, 100, linestyles = 'dashed', color = 'red', data = stockInfo.Date)
plt.hlines(50, 0, 100, linestyles = 'dashed', color = 'black', data = stockInfo.Date)

stockInfo['Sell Entry'] = ((stockInfo['%K'] < stockInfo['%D']) & (stockInfo['%K'].shift(1) > stockInfo['%D'].shift(1))) & (stockInfo['%D'] > 80) 
stockInfo['Sell Exit'] = ((stockInfo['%K'] > stockInfo['%D']) & (stockInfo['%K'].shift(1) < stockInfo['%D'].shift(1))) 
stockInfo['Short'] = np.nan 
stockInfo.loc[stockInfo['Sell Entry'],'Short'] = -1 
stockInfo.loc[stockInfo['Sell Exit'],'Short'] = 0 
stockInfo['Short'][0] = 0 
stockInfo['Short'] = stockInfo['Short'].fillna(method='pad') 
stockInfo['Buy Entry'] = ((stockInfo['%K'] > stockInfo['%D']) & (stockInfo['%K'].shift(1) < stockInfo['%D'].shift(1))) & (stockInfo['%D'] < 20) 
stockInfo['Buy Exit'] = ((stockInfo['%K'] < stockInfo['%D']) & (stockInfo['%K'].shift(1) > stockInfo['%D'].shift(1))) 
stockInfo['Long'] = np.nan  
stockInfo.loc[stockInfo['Buy Entry'],'Long'] = 1  
stockInfo.loc[stockInfo['Buy Exit'],'Long'] = 0  
stockInfo['Long'][0] = 0  
stockInfo['Long'] = stockInfo['Long'].fillna(method='pad') 

#Add Long and Short positions together to get final strategy position (1 for long, -1 for short and 0 for flat) 
stockInfo['Position'] = stockInfo['Long'] + stockInfo['Short']
stockInfo['Position'].plot(figsize=(20,10))

