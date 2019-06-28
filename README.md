# Stock_Analysis

Can you create mathematical and financial intuition based on current event articles, and past movement to predict short term stock movement?

### Prerequisites
    pip install pandas
    pip install matplotlib
    pip install numpy
    pip install jupyter
The program is written in Python 3.7

### Current Files
Stock_Visualization.ipynb was used as a preliminary analysis for analyzing the data given a stock and producing everyting subsequently.

Stock_Visualizations_Menu.py was modified from the jupyter notebook and designed as an object oriented class to pull different data and create some basic visualizations using matplotlib. I plan to use it as a baseline for different commands so when I build a web app or mobile application, different options selected for the reports will call different commands and functions.


### Current Capabilities
At it's current state, the program is capable of:

    - Pulling 100 days of data for a particular company
    
    - Pull a few days worth of data at intervals of n minutes for a particular stock
    
    - Convert the JSON data into a Pandas Dataframe that's easier to work with
    
    - Draw a Matplotlib line graph of the data with the option to display:
        - Closing Price
        - Open Price
        - Low Price
        - High Price
        - Volume
    
    - Calculate Stochastic Oscillation for the stock data and determine whether it may be a good time to long or short a stock
    
    - Draw out the Stochastic Oscillation for the stock data
    
    - Visualize the decision to Long, Short, or Hold a stock based on the Stochastic Oscillation
    
### TODO
    
    - Interactive visualization to zoom in out, look at values for a certain point in the map
    
    - Trying to find more details about a stock such as:
        - 52 Week High and Low (Yes, i'm aware I can calculate that myself)
        - Average Volume
        - Market Cap?
        - P/E Ratio
        - Div/Yield
    
    - Pulling general market information such as:
        - Dow Jones
        - Sector ratings
    
    - Temporarily serializing Pandas Dataframe containing Stock Info instead of having to constantly pull data from API
        - May be useful to use as a backup incase the computer is unable to make a connection to current data
    - Experiment with webscraping financial reports, quarterly earnings, articles, twitter messages
