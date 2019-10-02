# File Imports

# Library Imports
import re
import requests
import os
import csv
import shutil
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from nltk import ngrams
from nltk import FreqDist
from sklearn.model_selection import train_test_split
from time import sleep
from random import randint

# Note: Functions that begin with __ are private functions

class Federal_Reserve:
    # Public Methods
    def __init__(self):
        self.results = []

    def gather_articles_and_stock_info(self):
        """Gathers all article and stock info and writes them to files"""
        print('Gathering Articles')
        links2019 = self.__get_current_beige_links()
        links2011_ = self.__get_2011_to_previous_year_beige_links()
        monthly_links_2011_ = self.__get_2011_monthly_links(links2011_)
        monthly_links_1996_2011 = self.__get_1996_2011_monthly_links()
        __all_monthly_links = self.__compile_monthly_links(monthly_links_1996_2011,
                                                           monthly_links_2011_,
                                                           links2019)
        self.__get_stock_information()
        print('Finished Gathering Articles')

    def create_training_files(self, random_state=0):
        """Creates all the ngram data, computations, and files needed for testing"""
        try:
            self.__clear_previous_training_files()
            x_train, x_test = self.__split_files_for_training(random_state=random_state)
            self.__record_train_test_files(x_train, x_test)
            training_ngram_files = self.__create_ngram_files(x_train)
            training_files_sorted_by_n = self.__sort_ngram_files(training_ngram_files)
            self.__compute_increase_decrease_counts(training_files_sorted_by_n)
        except Exception as e:
            print('Error handling files.\nWill Delete Corrupted Files.\nRun Function again.')

    def test_program(self, neg_pos_ratio=0):
        """Takes in Testing files and executes testing"""
        testing_files = self.__get_testing_files()
        self.results.append(self.__test_program_with_articles(testing_files, neg_pos_ratio=neg_pos_ratio))


    # Private Methods
    def __split_files_for_training(self, train_size=0.8, test_size=0.2,
                                 random_state=7, shuffle=True):
        all_files = self.__get_all_article_file_names()
        x_train, x_test = train_test_split(all_files,
                                           train_size=train_size,
                                           test_size=test_size,
                                           random_state=random_state,
                                           shuffle=shuffle)
        return sorted(x_train), sorted(x_test)

    def __clear_previous_training_files(self):
        if os.path.exists(os.getcwd() + '/Federal_Reserve/Increase_Decrease'):
            shutil.rmtree(os.getcwd() + '/Federal_Reserve/Increase_Decrease')
        if os.path.exists(os.getcwd() + '/Federal_Reserve/NGrams'):
            shutil.rmtree(os.getcwd() + '/Federal_Reserve/NGrams')
        if os.path.exists(os.getcwd() + '/Federal_Reserve/Testing_Files_List.csv'):
            os.remove(os.getcwd() + '/Federal_Reserve/Testing_Files_List.csv')
        if os.path.exists(os.getcwd() + '/Federal_Reserve/Training_Files_List.csv'):
            os.remove(os.getcwd() + '/Federal_Reserve/Training_Files_List.csv')

    def __record_train_test_files(self, training_files, testing_files):
        training_file_name = str(os.getcwd() + '/Federal_Reserve/Training_Files_List.csv')
        testing_file_name = str(os.getcwd() + '/Federal_Reserve/Testing_Files_List.csv')

        with open(training_file_name, 'w') as txt_file:
            for file in training_files:
                txt_file.write(str(file + ','))

        with open(testing_file_name, 'w') as txt_file:
            for file in testing_files:
                txt_file.write(str(file + ','))


    def __create_ngram_files(self, all_files):
        ngram_file_names = []
        for file in all_files:
            date = self.__get_date_from_file_name(file)
            for n in range(1, 6):
                ngram_file_names.append(self.__get_ngrams(file, date, n))
        return ngram_file_names

    def __get_date_from_file_name(self, fileName):
        fullDate = {}
        date = fileName.split('/')[-1]
        date = date.split('_')[0]
        date = date.split('-')

        fullDate['year'] = date[0]
        fullDate['month'] = date[1]
        fullDate['day'] = date[2]

        return fullDate

    def __get_all_article_file_names(self):
        all_files = []

        article_path = (os.getcwd() + '/Federal_Reserve/Articles/')
        for root, dirs, files in os.walk(article_path):
            if files:
                for file in files:
                    fileName = root + '/' + file
                    all_files.append(fileName)

        return sorted(all_files)

    def __get_current_beige_links(self):
        """Gets links for Articles of the current year"""
        currentLinks = []
        currentURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-default.htm'
        sleep(3)
        page = requests.get(currentURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('td')

        for link in links:
            if re.match('.*htm.*', str(link)):
                link = str(link)
                link = link.split('"')
                if 'htm' in link[1]:
                    urlEnding = link[1].split('/')[-1]
                    currentLinks.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)
        return currentLinks

    def __get_2011_to_previous_year_beige_links(self):
        """Gets links for the archived years"""
        archiveURL = 'https://www.federalreserve.gov/monetarypolicy/beige-book-archive.htm'
        yearlyLinks = []
        try:
            sleep(3)
            page = requests.get(archiveURL)
            soup = BeautifulSoup(page.content, 'html.parser')
            links = soup.findAll(re.compile(r'a'))

            for link in links:
                if re.match('.*beigebook.*', str(link)):
                    link = str(link)
                    link = link.split('"')
                    urlEnding = link[1].split('/')[-1]
                    if ('htm' in link[1]):
                        yearlyLinks.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)

        except Exception as e:
            print("ERROR EXTRACTING YEAR URLS", e)

        return yearlyLinks

    def __get_2011_monthly_links(self, links2011_):
        """Get links from 2011 - (current year - 1)"""
        monthly_links = []
        for yearLink in links2011_:
            try:
                sleep(3)
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
                                monthly_links.append('https://www.federalreserve.gov/monetarypolicy/' + urlEnding)

                            elif (re.match(r'.*2011', urlEnding) or
                                  re.match(r'.*2012', urlEnding) or
                                  re.match(r'.*2013', urlEnding) or
                                  re.match(r'.*2014', urlEnding) or
                                  re.match(r'.*2015', urlEnding) or
                                  re.match(r'.*2016', urlEnding)):
                                monthly_links.append(
                                    'https://www.federalreserve.gov/monetarypolicy/beigebook/' + urlEnding)
                            else:
                                monthly_links.append(i[1])
            except Exception as e:
                print("ERROR GRABBING ARCHIVE MONTHS URLS", e)
        return monthly_links

    def __get_1996_2011_monthly_links(self):
        monthly_links = []
        for year in range(1996, 2011):
            base_url = f'https://www.federalreserve.gov/monetarypolicy/beigebook{year}.htm'
            try:
                sleep(3)
                page = requests.get(base_url)
                soup = BeautifulSoup(page.content, 'html.parser')
                links = soup.findAll('td')

                for link in links:
                    if re.match('.*htm.*', str(link)):
                        link = str(link)
                        link = link.split('"')
                        if 'htm' in link[1]:
                            monthly_links.append(link[1])
            except Exception as e:
                print("ERROR GRABBING ARCHIVE MONTHS URLS", e)
        return monthly_links

    def __compile_monthly_links(self,
                                monthly_links_2019,
                                monthly_links_2011_,
                                monthly_links_1996_2011):
        all_links = []

        for link in monthly_links_2019:
            all_links.append(link)
            try:
                self.__get_article_info(link)
            except Exception as e:
                print('ERROR EXTRACTING ARTICLE INFO:', e)

        for link in monthly_links_2011_:
            all_links.append(link)
            try:
                self.__get_article_info(link)
            except Exception as e:
                print('ERROR EXTRACTING ARTICLE INFO:', e)

        for link in monthly_links_1996_2011:
            all_links.append(link)
            try:
                self.__get_article_info(link)
            except Exception as e:
                print('ERROR EXTRACTING ARTICLE INFO:', e)


        return all_links

    def __get_article_info(self, url):
        print('Gathering Article Text From:', url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

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

        try:
            date = soup.find('title')
            date = date.get_text()
            date = date.split(' - ')
            date = str(date[-1])
            date = date.replace(',', '')
            newDate = date.split()

            month = self.__add_zero_to_date(months[newDate[0]])
            day = self.__add_zero_to_date(newDate[1])
            year = self.__add_zero_to_date(newDate[2])

        except Exception as e:
            # Will grab date for articles before 2011
            possibleDates = soup.findAll('strong')
            for date in possibleDates:
                date = date.get_text()
                if 'last update' in date.lower():
                    newDate = date.split(': ')[1]
                    newDate = newDate.replace(',', '')
                    newDate = newDate.split()
                    month = self.__add_zero_to_date(months[newDate[0]])
                    day = self.__add_zero_to_date(newDate[1])
                    year = self.__add_zero_to_date(newDate[2])

        # Check if Article folder exists, if not make it
        path = f"Federal_Reserve/Articles/{year}/"
        if not os.path.exists(path):
            os.makedirs(path)

        # Check if Article is already written if not, webscrape it and save it
        fileName = f"{path}{year}-{month}-{day}_Report.txt"
        if not os.path.exists(fileName):
            articleTag = soup.findAll('p')
            articleContent = ''
            for i in articleTag:
                articleContent += (i.get_text())

            file = open(fileName, "w+")
            file.write(articleContent)
            file.close()
            print("\nCreated", fileName)
            return fileName

    def __add_zero_to_date(self, date):
        if len(str(date)) == 1:
            return '0' + str(date)
        else:
            return date

    def __get_ngrams(self, articleFile, fullDate, n):
        """Takes in a file name and a number n to create a file with
            each ngram it produces"""

        month = fullDate['month']
        day = fullDate['day']
        year = fullDate['year']

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
            return fileName

    def __get_stock_information(self):
        marketPrices = {}
        dates = []
        for date in self.__get_all_article_file_names():
            tempDate = self.__get_date_from_file_name(date)
            dates.append(f'{tempDate["year"]}-{tempDate["month"]}-{tempDate["day"]}')
        dates = sorted(list(set(dates)))
        dates = self.__fix_month_and_days(dates)

        # Filter out training and testing articles
        marketData = pd.read_csv('Federal_Reserve/GSPC.csv')
        for date in dates:
            # Finds data of next closest trading day
            found_trading_day = self.__find_date_from_dataframe(date, marketData)
            data = marketData[(marketData.Date == date)]

            while found_trading_day == False:
                data = self.__increase_day_from_string(date)
                found_trading_day = self.__find_date_from_dataframe(data, marketData)
                data = marketData[(marketData.Date == date)]

            try:
                marketPrices[date] = {'Open': data.Open.values[0], 'High': data.High.values[0],
                                      'Low': data.Low.values[0], 'Close': data.Close.values[0],
                                      'Volume': data.Volume.values[0]}
            except Exception as e:
                print('Error loading market data for', date)

        self.__save_market_info(marketPrices)
        return marketPrices

    def __save_market_info(self, marketPrices):
        fileName = os.getcwd() + '/Federal_Reserve/Stock_History_Per_Article.csv'

        with open(fileName, 'w') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(('Date', 'Open', 'High', 'Low', 'Close', 'Volume'))
            for key, value in marketPrices.items():
                writer.writerow([key, value['Open'], value['High'],
                                 value['Low'], value['Close'],
                                 value['Volume']])
            print('Created', fileName)

    def __fix_month_and_days(self, dates):
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

    def __find_date_from_dataframe(self, date, marketData):
        data = marketData[(marketData.Date == date)]
        if len(data) > 0:
            return True
        else:
            return False

    def __increase_day_from_string(self, i):
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

    def __get_stock_history_from_csv(self):
        stock_info = {}
        fileName = str(os.getcwd() + '/Federal_Reserve/Stock_History_Per_Article.csv')
        if os.path.exists(fileName):
            reader = csv.DictReader(open(fileName))
            for row in reader:
                try:
                    stock_info[row['Date']] = {'Open': row['Open'],
                                          'High': row['High'],
                                          'Low': row['Low'],
                                          'Close': row['Close'],
                                          'Volume': row['Volume']}
                except KeyError:
                    pass
            return stock_info
        else:
            raise Exception("Stock Info not found, please gather all information first.")

    def __sort_ngram_files(self, ngramFiles):
        sorted_n = {}
        for file in ngramFiles:
            n = file.split('=')[1]
            n = n.split('.')[0]
            if n not in sorted_n:
                sorted_n[n] = [file]
            else:
                sorted_n[n].append(file)
        return sorted_n

    def __compute_increase_decrease_counts(self, sorted_ngram_files):
        stock_info = self.__get_stock_history_from_csv()
        for n, files in sorted_ngram_files.items():
            scored_ngrams = {}
            increase_ngrams = {}
            decrease_ngrams = {}
            print('\nn =', n)
            for file in range(len(files) - 1):
                try:
                    dates = files[file].split('/')[-1]
                    next_dates = files[file+1].split('/')[-1]
                    startDate = dates.split('_')[0]
                    endDate = next_dates.split('_')[0]
                    difference = float(stock_info[endDate]['Close']) - float(stock_info[startDate]['Close'])
                    year = startDate.split('-')[0]
                    reader = csv.DictReader(open(f'{os.getcwd()}/{files[file]}'))

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
                    pass

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

            self.__write_increase_decrease_files(n, scored_ngrams, ratio=False, increase=False)
            self.__write_increase_decrease_files(n, increase_ngrams, ratio=True, increase=True)
            self.__write_increase_decrease_files(n, decrease_ngrams, ratio=True, increase=False)

    def __write_increase_decrease_files(self, n, ngram_list, ratio=False, increase=False):
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

    def __get_testing_files(self):
        data = pd.read_csv(os.getcwd() + '/Federal_Reserve/Testing_Files_List.csv')
        return data.columns.tolist()

    def __test_program_with_articles(self, testingFiles, neg_pos_ratio=0.1):  # , stock_info):
        score = 0
        error = 0
        runs = len(testingFiles)

        for date in range(len(testingFiles)-1):
            try:
                fullDate = self.__get_date_from_file_name(testingFiles[date])
                article = (f'{os.getcwd()}/Federal_Reserve/Articles/{fullDate["year"]}/{fullDate["year"]}'
                           f'-{fullDate["month"]}-{fullDate["day"]}_Report.txt')

                print('\nArticle to Analyze:', article)

                with open(article) as file:
                    data = file.read()
                data = data.lower()

                increase_sum = 0
                decrease_sum = 0
                for n in range(1, 6):
                    ngramResult = ngrams(data.split(), n)
                    frequency = FreqDist(ngramResult).most_common()

                    articleNGrams = {}
                    for ngram in frequency:
                        words = ngram[0]
                        freq = ngram[1]
                        articleNGrams[f"{words}"] = freq

                    increase_ngrams = pd.read_csv(
                        os.getcwd() + f'/Federal_Reserve/Increase_Decrease/Increase_Ngrams/n={n}.csv')
                    increase_ngrams = increase_ngrams.set_index('NGram').T.to_dict('dict')

                    decrease_ngrams = pd.read_csv(
                        os.getcwd() + f'/Federal_Reserve/Increase_Decrease/Decrease_Ngrams/n={n}.csv')
                    decrease_ngrams = decrease_ngrams.set_index('NGram').T.to_dict('dict')

                    stock_history = pd.read_csv(os.getcwd() + '/Federal_Reserve/Stock_History_Per_Article.csv')
                    stock_history = stock_history.set_index('Date').T.to_dict('dict')

                    for ngram, freq in articleNGrams.items():
                        try:
                            if increase_ngrams[ngram]:
                                increase_sum += (increase_ngrams[ngram]['Increase_Weight'] * freq)
                        except KeyError:
                            pass

                        try:
                            if decrease_ngrams[ngram]:
                                decrease_sum += (decrease_ngrams[ngram]['Decrease_Weight'] * freq)
                        except KeyError:
                            pass
                    # print(f'\nN = {n}')
                    # print('Increase Sum:', increase_sum)
                    # print('Decrease Sum:', decrease_sum)

                # Get actual stock movement between current period
                acutalStockMovement = -1
                actualStockChange = 0
                listStockHistory = list(stock_history)
                for reportDate in range(len(listStockHistory)):
                    if f'{fullDate["year"]}-{fullDate["month"]}' in listStockHistory[reportDate]:
                        startDate = listStockHistory[reportDate]
                        endDate = listStockHistory[reportDate + 1]
                        startPrice = stock_history[startDate]['Close']
                        endPrice = stock_history[endDate]['Close']

                        if endPrice - startPrice > 0:
                            acutalStockMovement = 1
                        actualStockChange = endPrice - startPrice
                    else:
                        pass

                predictedStockMovement = -1
                # If the postive greatly outweighs negative, the article is considered positive
                if (decrease_sum / increase_sum) < neg_pos_ratio:
                    predictedStockMovement = 1

                print('Increase Sum:', increase_sum)
                print('Decrease Sum:', decrease_sum)
                print('Inc - Dec Ratio:', (decrease_sum / increase_sum))
                print(f'Stock Movement: {actualStockChange}')
                print(f'Predicted Movement: {predictedStockMovement} Actual Movement: {acutalStockMovement}')

                if predictedStockMovement == acutalStockMovement:
                    score += 1
                error += (predictedStockMovement - acutalStockMovement)
            except Exception as e:
                print('ERROR:', e)
        percent_score = ((score/runs) * 100)
        print(f'\nTotal Score: {percent_score}% Accuracy of {runs} Runs')
        print(f'Total Error: {error}')

        return (f'{percent_score}, {runs}, {error}, {neg_pos_ratio}')

    def print_results(self):
        for i in self.results:
            print(i)


fed = Federal_Reserve()
fed.create_training_files(random_state=9)
fed.test_program(neg_pos_ratio=0.05)
fed.print_results()



