import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import json
from pandas.io.json import json_normalize

from APIData import getAPIKey

apiKey = getAPIKey()
symbol = 'TSLA'
type = 'TIME_SERIES_DAILY'
url = f'https://www.alphavantage.co/query?function={type}&symbol={symbol}&apikey={apiKey}'

with urllib.request.urlopen(url) as response:
   html = response.read()
   data = json.loads(html)

df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
print(df.head())
