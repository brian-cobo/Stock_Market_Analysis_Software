# Stock_Market_Analysis_Software

Can you create mathematical and financial intuition based on current event articles, and past movement to predict short term stock movement?

### Vision
To create software that is capable of automatically gathering and analyzing information about companies to provide the user an opinion on any stock based on facts, data, and predictions.

### Prerequisites
    pip install bs4
    pip install jupyter
    pip install matplotlib
    pip install nltk
    pip install numpy
    pip install pandas
    pip install scikit-learn
Requires API Key from https://www.alphavantage.co

### Current Files
* Python Files
    * Stock_Visualizations_Menu.py
        * Serves as the main program for the project
        * Collects and displays information collected from stocks
        * Can draw graphs and oscillations based on the info
        * Uses alpha vantage api for getting stock data
    * NLTK-Sentiment-Analysis.py
        * Collects article information from ibtimes
        * Script has the option of searching for companies specifically and saving the information or saving the articles on the first page of the business section
        * The article body is analyzed using NLTK to produce a sentiment value on the scale of -1 (Highly Negative) to 1 (Highly Positive)
        * The collected information is currently saved in a csv file, with extra resources, I would host a database storing the information
    
### TODO
#### Main
* Automate the data cleaning for better analysis
* Analyze and improve accuracy of Sentiment Analysis to be correct and recognize financial vocabulary
* Provide visualizations of Sentiment Analysis results
* Gathering Dow Jones and other market information
* Web Scrape and Analyze 
    * Financial reports
    * Quarterly Earnings
* Create a user interface to steer away from command line use
* Proving a correlation between average sentiment analysis and stock movment using T Tests and other statistical methods
* Analyzing common words and phrases between articles with similar ratings that may provide indication to the performance of a stock
* Create a single model comprised of models that look at various aspects of stock data to try and come to an average consensus about future performance
    * Create a model to predict movement based on Sentiment Analysis and past data
    * Create a model to predict movement solely based on past data
    * Create a model looking at volume of stock based on highs, lows, opens, and closes?
* Create an automated report discussing findings, data, numbers, predictions, and an overall opinion on stock movment in the near future and whether it'd be worth buying
* Create a visualized test following a companies history and what the model suggests and see how accurate it is, and how much it yields
* Create a report based on the research project to discuss findings, possible future ideas, possible sources of errors and how to improve

#### Optional
* Interactive visualization to zoom in out, look at values for a certain point in the map  
* Trying to find more details about a stock such as:
    * 52 Week High and Low (Yes, i'm aware I can calculate that myself)
    * Average Volume
    * Market Cap?
    * P/E Ratio
    * Div/Yield
    * Any Greek Values for Option Trading?
* Temporarily serializing Pandas Dataframe containing Stock Info instead of having to constantly pull data from API
    * May be useful to use as a backup in case the computer is unable to make a connection to current data
* Create and host a database to store information gathered and produced
    

### Sources Used
* https://sraf.nd.edu
    * Used for Financial Sentiment Analysis
        * Used their code and dictionary to analyze financial lexicon
* https://www.dataquest.io/blog/web-scraping-tutorial-python/
    * Used for building the webscraper
* http://www.nltk.org/howto/sentiment.html
    * Documentation for the NLTK library
* https://pythonforfinance.net/2017/10/10/stochastic-oscillator-trading-strategy-backtest-in-python/
    * Stochastic Oscillator Code
