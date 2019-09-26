# File Imports

# Library Imports
import re
import requests
import os
import csv
import pandas as pd

from bs4 import BeautifulSoup
from nltk import ngrams
from nltk import FreqDist
from time import sleep
from random import randint

"""
NOTES:
I'm still working out some issues with the webscraping part. 
At the moment I have the webscraper for 2019 working correctly, i'm having some issues 
with the archive stuff since the formats for the URLs and the sites vary between years. 
I should have 2011-2018 working correctly soon. Earlier articles will take a lot more effort
since the URLs are more advanced and require specific dates as a part of them. I can work
on that if you find value for it, if not I can hold off on it. I'm taking the articles, and
running the through a function to get the ngrams. I'm currently generating unigrams through
sextagrams (not sure if that's the correct name, but it sounds right) and printing them.

ALGORITHM:
* Read in https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm HTML code
* Look for the table rows which contains links to all the articles written this year
* Append that to a list that will hold all Monthly URLs
* Extract article content by looking for P tags in the HTML
* Add content to a string
* Create NGrams with N looping from 1 - 6
* Print NGram

TODO:
* Rather than rely on URL to grab article, I want to write the article to a text file.
    * Doing so will make it a bit faster to read and create the n grams and we can
      specify which article we can look at.
* Fix the 2011-2018 webscraper portions
* Come up with better ngram output. Possibly writing each ngram to a file per URL
* Want to look at Ngram for all articles combined
    * Writing articles to text files will help with that
"""


# Archive Home
# https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm

# 2019 Home
# https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm

# URLs separated by URL pattern

# Jan 16, 2019 https://www.federalreserve.gov/monetarypolicy/beigebook201901.htm
# Jan 17, 2018 https://www.federalreserve.gov/monetarypolicy/beigebook201801.htm
# Jan 18, 2017 https://www.federalreserve.gov/monetarypolicy/beigebook201701.htm

# Jan 13, 2016 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201601.htm
#              https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201601.htm?summary
# Jan 14, 2015 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201501.htm
# Jan 14, 2014 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201401.htm
# Jan 16, 2013 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201301.htm
# Jan   , 2012 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201201.htm
# Jan 12, 2011 https://www.federalreserve.gov/monetarypolicy/beigebook/beigebook201101.htm

# Jan 13, 2010 https://www.federalreserve.gov/fomc/beigebook/2010/20100113/default.htm
# Jan 14, 2009 https://www.federalreserve.gov/fomc/beigebook/2009/20090114/FullReport.htm
#              https://www.federalreserve.gov/fomc/beigebook/2009/20090114/default.htm
# Jan 17, 2007 https://www.federalreserve.gov/fomc/beigebook/2007/20070117/FullReport.htm
# Jan 19, 2005 https://www.federalreserve.gov/fomc/beigebook/2005/20050119/FullReport.htm
#              https://www.federalreserve.gov/fomc/beigebook/2005/20050119/default.htm
# Jan 22, 1997 https://www.federalreserve.gov/fomc/beigebook/1997/19970122/default.htm


def get_2019_beige_links(currentURL):
    """Gets links for 2019 Articles"""
    print('Scraping 2019 Articles')
    currentLinks = []
    currentURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm'
    page = requests.get(currentURL)
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.findAll('td')
    for i in links:
        if re.match('.*htm.*', str(i)):
            i = str(i)
            i = i.split('"')
            if 'htm' in i[1]:
                urlEnding = i[1].split('/')[-1]
                currentLinks.append('https://www.federalreserve.gov/monetarypolicy/'+ urlEnding)
    return currentLinks


def get_archive_beige_links():
    """Gets links for the archived years"""
    archiveURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm'
    yearlyLinks = []
    monthlyLinks = []
    try:
        page = requests.get(archiveURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll(re.compile(r'a'))
        for i in links:
            if re.match('.*beigebook.*', str(i)):
                i = str(i)
                i = i.split('"')
                if 'htm' in i[1]:
                    urlEnding = i[1].split('/')[-1]
                    yearlyLinks.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)
    except Exception as e:
        print("ERROR EXTRACTING YEAR URLS", e)

    for yearLink in yearlyLinks:
        try:
            sleep(3)
            print('Scraping', yearLink)
            page = requests.get(yearLink)
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.findAll('td')
            for i in links:
                if re.match('.*htm.*', str(i)) and \
                        'default' not in str(i):
                    i = str(i)
                    i = i.split('"')
                    if 'htm' in i[1]:
                        urlEnding = i[1].split('/')[-1]
                        if (re.match(r'.*2018', urlEnding) or
                                re.match(r'.*2017', urlEnding)):
                            monthlyLinks.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)
                        elif (re.match(r'.*2011', urlEnding) or
                                  re.match(r'.*2012', urlEnding) or
                                  re.match(r'.*2013', urlEnding) or
                                  re.match(r'.*2014', urlEnding) or
                                  re.match(r'.*2015', urlEnding) or
                                  re.match(r'.*2016', urlEnding)):
                            monthlyLinks.append('https://www.federalreserve.gov/monetarypolicy/beigebook/' + urlEnding)
                        else:
                            break
        except Exception as e:
            print("ERROR GRABBING ARCHIVE MONTHS URLS", e)
    return monthlyLinks


def add_zero_to_date(date):
    if len(str(date)) == 1:
        return '0' + str(date)
    else:
        return date


def get_ngrams(articleFile, fullDate, n):
    """Takes in a file name and a number n to create a file with
        each ngram it produces"""
    months = {'January': 1,
              'February': 2,
              'March': 3,
              'April': 4,
              'May': 5,
              'June': 6,
              'July': 7,
              'August': 8,
              'September': 9,
              'October': 10,
              'November': 11,
              'December': 12}

    month = add_zero_to_date(months[fullDate[0]])
    day = add_zero_to_date(fullDate[1])
    year = add_zero_to_date(fullDate[2])

    # Check if ngram folder exists, if not make it
    path = f"Federal_Reserve/NGrams/{year}/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Check if ngram file exists, if not write it
    fileName = f"{path}{year}-{month}-{day}_ngram_n={n}.csv"
    if not os.path.exists(fileName):
        with open(articleFile) as articlefile:
            article = articlefile.read()
        article = re.sub(r'([^\s\w]|_)+', '', article)
        article = article.lower()
        ngramsResult = ngrams(article.split(), n)
        frequency = FreqDist(ngramsResult).most_common()

        articleNGrams = {}
        for ngram in frequency:
            words = ngram[0]
            freq = ngram[1]
            articleNGrams[words] = freq

        with open(fileName, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('NGram', 'Frequency'))
            for key, value in articleNGrams.items():
                writer.writerow([key, value])
        print('Created', fileName)


def get_article_info(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    date = soup.find('title')
    date = date.get_text()
    date = date.split(' - ')
    date = str(date[-1])
    date = date.replace(',', '')
    fullDate = date.split()

    months = {'January' : 1,
              'February' : 2,
              'March' : 3,
              'April' : 4,
              'May' : 5,
              'June' : 6,
              'July' : 7,
              'August' : 8,
              'September' : 9,
              'October' : 10,
              'November': 11,
              'December': 12}

    month = add_zero_to_date(months[fullDate[0]])
    day = add_zero_to_date(fullDate[1])
    year = add_zero_to_date(fullDate[2])

    # Check if Article folder exists, if not make it
    path = f"Federal_Reserve/Articles/{year}/"
    if not os.path.exists(path):
        os.makedirs(path)

    # Check if Article is already written if not, webscrape it and save it
    fileName = f"{path}{year}-{month}-{day}_Report.txt"
    if not os.path.exists(fileName):
        # page = requests.get(url)
        # soup = BeautifulSoup(page.content, 'html.parser')
        articleTag = soup.findAll('p')
        articleContent = ''
        for i in articleTag:
            articleContent += (i.get_text())

        file = open(fileName, "w+")
        file.write(articleContent)
        file.close()
        print("\nCreated", fileName)

        for i in range(1, 6):
            get_ngrams(fileName, fullDate, i)


def find_date_from_dataframe(date, marketData):
    data = marketData[(marketData.Date == date)]
    if len(data) > 0:
        return True
    else:
        return False


def increase_day_from_string(i):
    day = int(i.split('-')[-1])
    if (day + 1) > 30:
        day = 1
    else:
        day += 1
        day = '0' + str(day)
    i = i.split('-')
    i[-1] = str(day)
    i = ('-').join(i)
    return i


def fix_month_and_days(dates):
    fixed_dates = []
    for date in dates:
        newDate = date.split('-')
        # Adding 0 to beginning of month if len = 1
        if len(newDate[1]) == 1:
            newDate[1] = '0' + newDate[1]
        if len(newDate[2]) == 1:
            newDate[2] = '0' + newDate[2]
        newDate = ('-').join(newDate)
        fixed_dates.append(newDate)
    return fixed_dates


def save_market_info(marketPrices):
    fileName = os.getcwd() + '/Federal_Reserve/Stock_History.csv'

    with open(fileName, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Date', 'Open', 'High', 'Low', 'Close', 'Volume'))
        for key, value in marketPrices.items():
            writer.writerow([key, value['Open'], value['High'],
                             value['Low'], value['Close'],
                             value['Volume']])
        print('Created', fileName)


def collect_stock_information():
    ngramFiles = []
    dates = []
    marketPrices = {}
    path = 'Federal_Reserve/NGrams/'
    for i in os.walk(path):
        if i[2]:
            for file in i[2]:
                ngramFiles.append(file)

    ngramFiles = sorted(ngramFiles)
    for i in ngramFiles:
        date = i.split('_')[0]
        dates.append(date)

    dates = sorted(list(set(dates)))
    dates = fix_month_and_days(dates)
    marketData = pd.read_csv('Federal_Reserve/GSPC.csv')

    print('Number of Original Dates:', len(dates))
    for date in dates:
        # Finds data of next closest trading day
        found_trading_day = find_date_from_dataframe(date, marketData)
        data = marketData[(marketData.Date == date)]

        while found_trading_day == False:
            data = increase_day_from_string(date)
            found_trading_day = find_date_from_dataframe(data, marketData)
            data = marketData[(marketData.Date == date)]

        try:
            marketPrices[date] = {'Open': data.Open.values[0], 'High': data.High.values[0],
                                  'Low': data.Low.values[0], 'Close': data.Close.values[0],
                                  'Volume': data.Volume.values[0]}
        except Exception as e:
            print('Error loading market data for', date)

    save_market_info(marketPrices)
    return ngramFiles, marketPrices


def sort_ngram_files(ngramFiles):
    sorted_n = {}
    for file in ngramFiles:
        n = file.split('=')[1]
        n = n.split('.')[0]
        if n not in sorted_n:
            sorted_n[n] = [file]
        else:
            sorted_n[n].append(file)
    return sorted_n


def get_monthly_links(webscrape=False):
    if webscrape:
        monthURL = []
        links2019 = get_2019_beige_links(currentURL='https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm')
        linksArchive = get_archive_beige_links()

        for i in links2019:
            monthURL.append(i)
        for i in linksArchive:
            monthURL.append(i)
        for i in monthURL:
            try:
                get_article_info(i)
            except Exception as e:
                print(e)


def write_increase_decrease_files(n, ngram_list, ratio=False, increase=False):
    paths = [f"{os.getcwd()}/Federal_Reserve/Increase_Decrease/Increase_Ngrams/",
             f"{os.getcwd()}/Federal_Reserve/Increase_Decrease/Decrease_Ngrams/",
             f"{os.getcwd()}/Federal_Reserve/Increase_Decrease/All_Ngrams/"]
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)

    if ratio and increase:
        fileName = f'{os.getcwd()}/Federal_Reserve/Increase_Decrease/Increase_Ngrams/n={n}.csv'
    elif ratio and not increase:
        fileName = f'{os.getcwd()}/Federal_Reserve/Increase_Decrease/Decrease_Ngrams/n={n}.csv'
    else:
        fileName = f'{os.getcwd()}/Federal_Reserve/Increase_Decrease/All_Ngrams/n={n}.csv'


    with open(fileName, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('NGram', 'Increase', 'Decrease',
                         'Increase_Weight', 'Decrease_Weight',
                         'Increase_Ratio', 'Decrease_Ratio'))
        for key, value in ngram_list.items():
            writer.writerow([key, value['Increase'], value['Decrease'],
                             value['Increase_Weight'], value['Decrease_Weight'],
                             value['Increase_Ratio'], value['Decrease_Ratio']])
        print('Created', fileName)


def compute_increase_decrease_counts(sorted_ngram_files, stock_info):
    for n, files in sorted_ngram_files.items():
        scored_ngrams = {}
        increase_ngrams = {}
        decrease_ngrams = {}
        print('\nn =', n)
        for file in range(len(files)-1):
            try:
                startDate = files[file].split('_')[0]
                endDate = files[file+1].split('_')[0]
                difference = stock_info[endDate]['Close'] - stock_info[startDate]['Close']
                year = files[file].split('-')[0]
                reader = csv.DictReader(open(f'{os.getcwd()}/Federal_Reserve/NGrams/{year}/{files[file]}'))

                if difference > 0:
                    for row in reader:
                        if row['NGram'] not in scored_ngrams:
                            scored_ngrams[(row['NGram'])] = {'Increase': int(row['Frequency']), 'Decrease': 0,
                                                             'Increase_Weight': 0, 'Decrease_Weight': 0,
                                                             'Increase_Ratio': 0, 'Decrease_Ratio': 0}
                        else:
                            scored_ngrams[(row['NGram'])]['Increase'] += int(row['Frequency'])

                else:
                    for row in reader:
                        if row['NGram'] not in scored_ngrams:
                            scored_ngrams[(row['NGram'])] = {'Increase': 0, 'Decrease': int(row['Frequency']),
                                                             'Increase_Weight': 0, 'Decrease_Weight': 0,
                                                             'Increase_Ratio': 0, 'Decrease_Ratio': 0}
                        else:
                            scored_ngrams[(row['NGram'])]['Decrease'] += int(row['Frequency'])
            except Exception as e:
                print('Error handling', files[file])

        for ngram, value in scored_ngrams.items():
            increase = value['Increase']
            decrease = value['Decrease']
            value['Increase_Weight'] = round(float(increase / (increase + decrease)), 5)
            value['Decrease_Weight'] = round(float(decrease / (increase + decrease)), 5)
            try:
                value['Increase_Ratio'] = round(float(value['Increase_Weight'] / value['Decrease_Weight']))
            except ZeroDivisionError:
                value['Increase_Ratio'] = 0
            try:
                value['Decrease_Ratio'] = round(float(value['Decrease_Weight'] / value['Increase_Weight']))
            except ZeroDivisionError:
                value['Decrease_Ratio'] = 0

            if value['Increase_Ratio'] >= 3:
                increase_ngrams[ngram] = value

            if value['Decrease_Ratio'] >= 3:
                decrease_ngrams[ngram] = value

        write_increase_decrease_files(n, scored_ngrams, ratio=False, increase=False)
        write_increase_decrease_files(n, increase_ngrams, ratio=True, increase=True)
        write_increase_decrease_files(n, decrease_ngrams, ratio=True, increase=False)


def test_program_with_articles(n): #, stock_info):
    # Chooses random article to analyze
    year = randint(2011, 2019)
    articlePath = str(os.getcwd() + f'/Federal_Reserve/Articles/{year}/')
    articlesInPath = os.listdir(articlePath)
    articleToAnalyze = randint(0, len(articlesInPath) - 1)
    articleTitle = articlesInPath[articleToAnalyze]
    date = articleTitle.split('_')[0]
    article = articlePath + articleTitle
    print('Article to Analyze:', articleTitle)

    with open(article) as file:
        data = file.read()
    data = data.lower()

    ngramResult = ngrams(data.split(), n)
    frequency = FreqDist(ngramResult).most_common()

    articleNGrams = {}
    for ngram in frequency:
        words = ngram[0]
        freq = ngram[1]
        articleNGrams[words] = freq

    increase_ngrams = pd.read_csv(os.getcwd() + f'/Federal_Reserve/Increase_Decrease/Increase_Ngrams/n={n}.csv')
    increase_ngrams = increase_ngrams.set_index('NGram').T.to_dict('dict')

    decrease_ngrams = pd.read_csv(os.getcwd() + f'/Federal_Reserve/Increase_Decrease/Decrease_Ngrams/n={n}.csv')
    decrease_ngrams = decrease_ngrams.set_index('NGram').T.to_dict('dict')

    stock_history = pd.read_csv(os.getcwd() + '/Federal_Reserve/Stock_History.csv')

    sum = 0
    for ngram, freq in articleNGrams.items():
        try:
            if increase_ngrams[ngram]:
                print('Ngram:', ngram, 'In increase ngrams')
                print(increase_ngrams[ngram])
                sum += (increase_ngrams['Increase_Weight'] * freq)
                print('New Sum:', sum)
        except KeyError:
            pass

        try:
            if decrease_ngrams[ngram]:
                print('Ngram:', ngram, 'In decrease ngrams')
                print(decrease_ngrams[ngram])
                sum -= (decrease_ngrams['Increase_Weight'] * freq)
        except KeyError:
            pass
    print('Article Total:', sum)


get_monthly_links(webscrape=True)
ngramsFiles, stock_info = collect_stock_information()
sorted_ngram_files = sort_ngram_files(ngramsFiles)
compute_increase_decrease_counts(sorted_ngram_files, stock_info)
test_program_with_articles(1)
test_program_with_articles(2)
test_program_with_articles(3)
test_program_with_articles(4)
test_program_with_articles(5)
