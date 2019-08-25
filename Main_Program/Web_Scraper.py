# File Imports
from Main_Program.Stock_Visualizations_Menu import search_for_company_symbol
from Main_Program.Sentiment_Analyzer import parser

# Library Imports
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import re


#TODO
# Analyze company earnings reports
#       Twitter Example
#       https://www.nasdaq.com/aspx/stockmarketnewsstoryprint.aspx?storyid=twitter-announces-second-quarter-2019-results-20190726-00186


class Webscraper:
    """This class deals with extracting info from articles and saving them"""
    def add_row_to_saved_article_results_dataframe(self, article_info):
        """If it turns out that the article it analyzes isn't already in the
            Sentiments_Results.csv file, this function will add the information
            gathered into the csv file"""
        if (self.check_for_existing_article_results(article_info['URL']) == False and
                self.check_for_null_values(article_info) == True):
            article_results_dataframe = self.return_article_results_dataframe()
            article_results_dataframe = article_results_dataframe.append(
                                             {'URL': article_info['URL'],
                                              'Title': article_info['Title'],
                                              'Company_Symbol': article_info['Company_Symbol'],
                                              'Author': article_info['Author'],
                                              'Date_Published': article_info['Date_Published'],
                                              'Time_Published': article_info['Time_Published'],
                                              'numberOfWords': article_info['numberOfWords'],
                                              'positive_%': article_info['positive_%'],
                                              'negative_%': article_info['negative_%'],
                                              'uncertainty_%': article_info['uncertainty_%'],
                                              'litigious': article_info['litigious'],
                                              'modal-weak_%': article_info['modal-weak_%'],
                                              'modal-moderate_%': article_info['modal-moderate_%'],
                                              'modal-strong_%': article_info['modal-strong_%'],
                                              'constraining_%': article_info['constraining_%'],
                                              'num_of_alphanumeric': article_info['num_of_alphanumeric'],
                                              'num_of_digits': article_info['num_of_digits'],
                                              'num_of_Numbers': article_info['num_of_Numbers'] ,
                                              'avg_num_Of_syllables_per_word': article_info['avg_num_Of_syllables_per_word'],
                                              'avg_word_length': article_info['avg_word_length'],
                                              'vocabulary': article_info['vocabulary']
                                             },
                                             ignore_index=True)
            self.clean_article_results_columns(article_results_dataframe)
        else:
            if self.check_for_null_values(article_info) == False:
                print('Not all values were found correctly, not saving:', article_info['URL'])
            else:
                print('Article Info Already Saved')

    def check_for_null_values(self, article_info):
        """Check to see if the entire result of the webscraper is null"""
        if (article_info['URL'] != None and
                article_info['Title'] != None and
                article_info['Company_Symbol'] != None and
                article_info['Author'] != None and
                article_info['Date_Published'] != None and
                article_info['Time_Published'] != None):
            return True
        else:
            return False

    def clean_article_results_columns(self, article_results_dataframe):
        """For some reason, each append to the csv file created a new column, so the
            code is removing the columns that we don't want to save"""
        columns = ['URL', 'Title', 'Company_Symbol', 'Author',
                   'Date_Published', 'Time_Published', 'numberOfWords',
                   'positive_%', 'negative_%', 'uncertainty_%',
                   'litigious', 'modal-weak_%', 'modal-moderate_%',
                    'modal-strong_%', 'constraining_%', 'num_of_alphanumeric',
                    'num_of_digits', 'num_of_Numbers', 'avg_num_Of_syllables_per_word',
                    'avg_word_length', 'vocabulary']

        for column in article_results_dataframe.columns:
            if column not in columns:
                article_results_dataframe = article_results_dataframe.drop(columns=[column], axis=1)
                article_results_dataframe.to_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
        article_results_dataframe.to_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
        return article_results_dataframe

    def create_saved_article_results_dataframe(self):
        """Creates new CSV file with the columns listed below"""
        article = pd.DataFrame(columns=['URL',
                                        'Title',
                                        'Company_Symbol',
                                        'Author',
                                        'Date_Published',
                                        'Time_Published',
                                        'numberOfWords',
                                        'positive_%',
                                        'negative_%',
                                        'uncertainty_%',
                                        'litigious',
                                        'modal-weak_%',
                                        'modal-moderate_%',
                                        'modal-strong_%',
                                        'constraining_%',
                                        'num_of_alphanumeric',
                                        'num_of_digits',
                                        'num_of_Numbers',
                                        'avg_num_Of_syllables_per_word',
                                        'avg_word_length',
                                        'vocabulary'])
        article.to_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
        return article

    def return_article_results_dataframe(self):
        """Check to see if csv file exists, if not create a new one"""
        article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
        if os.path.exists(article_result_file_path):
            saved_article_results = pd.read_csv(article_result_file_path)
            if len(saved_article_results) > 0:
                return saved_article_results
            else:
                return self.create_saved_article_results_dataframe()
        return self.create_saved_article_results_dataframe()


    def check_for_existing_article_results(self, URL_to_check_for):
        """ Check to see if URL extracted from webscraper already exists in the csv file"""
        article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
        if os.path.exists(article_result_file_path):
            article = pd.read_csv(article_result_file_path)
            data = article[(article.URL == URL_to_check_for)]
            if len(data) > 0:
                return True
            else:
                return False
        return False

    def get_sentiment_analysis(self, article_info):
        """Calls to Main_Program.Sentiment_Analyzer.parser to analyze article
            and adds the results to the article_info dictionary"""
        article = article_info['Article'][0]
        article_results = parser(article)

        article_info['numberOfWords'] = article_results['numberOfWords']
        article_info['positive_%'] = article_results['positive_%']
        article_info['negative_%'] = article_results['negative_%']
        article_info['uncertainty_%'] = article_results['uncertainty_%']
        article_info['litigious'] = article_results['litigious']
        article_info['modal-weak_%'] = article_results['modal-weak_%']
        article_info['modal-moderate_%'] = article_results['modal-moderate_%']
        article_info['modal-strong_%'] = article_results['modal-strong_%']
        article_info['constraining_%'] = article_results['constraining_%']
        article_info['num_of_alphanumeric'] = article_results['num_of_alphanumeric']
        article_info['num_of_digits'] = article_results['num_of_digits']
        article_info['num_of_Numbers'] = article_results['num_of_Numbers']
        article_info['avg_num_Of_syllables_per_word'] = article_results['avg_num_Of_syllables_per_word']
        article_info['avg_word_length'] = article_results['avg_word_length']
        article_info['vocabulary'] = article_results['vocabulary']

        return article_info

    def find_title_from_article(self, soup):
        """Finds Title tag from HTML"""
        return soup.find_all('title')[0].get_text()

    def find_author_from_article(self, soup):
        """Finds Span tag, and name property from HTML"""
        return soup.find_all('span', itemprop='name')[0].get_text()

    def find_publish_date_and_time_from_article(self, soup):
        """Finds Time tag and date published property from
            HTML and separates the date and time"""
        time = soup.find_all('time', itemprop='datePublished')
        published_time = ''
        for i in time:
            published_time += i.get_text()
        published_time = published_time.split()
        date_published = published_time[0]
        time_published = (' ').join(published_time[2:4])
        return (date_published, time_published)

    def find_article_content(self, soup):
        """Finds Article by looking for P tags in HTML"""
        tag = soup.find_all('p')
        article = ''
        for i in tag:
            article += (i.get_text())
        return [article]

    def find_company_symbol_from_article(self, soup, title, article_content):
        """This is a tricky one.
            Most articles won't state the symbol of the
            company they're writing about, so I'm searching through the metadata
            for their keywords. To try to ensure the symbol I extract is accurate:
                * I take all the keywords and put them into a frequency map to see which
                  keywords show up the most
                * I iterate through the keywords and search for them using a function
                  which takes in a string and searches for possible company matches
                  to retrieve the company symbol. With the symbol and company name
                  it produces, It checks:
                   * That the keyword is in the title
                   * The keyword is in the article somewhere
                   * The symbol results' company is located in the US by looking at the currency
                   * The name of the symbol results' company is located in the article at least twice
                * If the 4 condititions above are not met, it will iterate through the list of keywords
                   found in the meta data.
                    * If no company names are found, it returns None and the article will not be saved

            Note: * This algorithm is not perfect and does find company symbols that satisfies all conditions
                    that are incorrect.
                  * The algorithm also produces incorrect results when multiple company
                    names are found in the article and title.
                  * The algorithm can be refined, however, for articles where the company name shows up
                    in the meta data, it finds the company symbol accurately.
        """
        company_symbol = None
        company = soup.find_all('meta')
        for i in company:
            if 'keywords' in str(i):
                i = str(i)
                i = i.split('="')[1]
                i = i.split()
                for item in range(len(i)):
                    regex = re.compile('[^a-zA-Z]')
                    i[item] = regex.sub('', i[item])
                count = Counter(i)
                for key, value in count.items():
                    try:
                        if company_symbol == None:
                            symbols = search_for_company_symbol(key, automated=True)
                            if (key in title.lower() and
                                    key in article_content[0].lower() and
                                    key in symbols.Name.iloc[0].lower() and
                                    symbols.Currency.iloc[0] == 'USD' and
                                    article_content[0].count(symbols.Name.iloc[0].split()[0]) > 1):
                                company_symbol = symbols.Symbol.iloc[0]

                    except Exception as e:
                        pass
                break
        return company_symbol

    def print_dictionary(self, dict):
        """Prints each key and value for dictionaries passed in"""
        print()
        for key, value in dict.items():
            print(key, ':', value)

    def scrape_article_from_web(self, article_URL):
        """Given a url, it calls out to other functions to extract article info
           and returns the info """
        try:
            page = requests.get(article_URL)-1
            soup = BeautifulSoup(page.content, 'html.parser')

            title = self.find_title_from_article(soup)
            author = self.find_author_from_article(soup)
            date_published, time_published = self.find_publish_date_and_time_from_article(soup)
            article_content = self.find_article_content(soup)
            company_symbol = self.find_company_symbol_from_article(soup, title, article_content)

            article_extracted_info = {'URL' : article_URL,
                                      'Title' : title,
                                      'Company_Symbol': company_symbol,
                                      'Author': author,
                                      'Date_Published' : date_published,
                                      'Time_Published' : time_published,
                                      'Article' : article_content}
            return(article_extracted_info)
        except Exception as e:
            print(e)


class Find_Articles:
    """This class deals with finding the URLs to the articles to be extracted"""
    def find_search_URL(self, string_to_search_for):
        """I found the algorithm for searches at ibtimes.com and use that so that I can turn
            the string to search info for into a URL I can use to grab the article URLS"""
        search = string_to_search_for.replace(' ', '%20')
        search_URL = 'https://www.ibtimes.com/search/site/' + search
        print(search_URL)
        return search_URL

    def find_article_from_search_URL(self, search_URL, numPages=1):
        """Given a search URL, it finds all the article URLs and sends them to get extracted"""
        page = requests.get(search_URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        links = soup.findAll('a', attrs={'href': re.compile("^https://")})
        for link in links:
            newLink = link.get('href')
            if ('twitter.com' not in newLink and
                'facebook.com' not in newLink and
                'linkedin.com' not in newLink and
                'ibtimes.tumblr.com' not in newLink):
                self.scrape_analyze_store_article(newLink)

        self.search_multiple_pages(search_URL, numPages)

    def search_multiple_pages(self, search_URL, num_of_pages=1):
        """Retrieves URLs from n number of pages given a search URL"""
        for i in range(1,num_of_pages):
            try:
                URL = search_URL + f'?page={i}'
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, 'html.parser')
                links = soup.findAll('a', attrs={'href': re.compile("^https://")})
                for link in links:
                    newLink = link.get('href')
                    if ('twitter.com' not in newLink and
                            'facebook.com' not in newLink and
                            'linkedin.com' not in newLink and
                            'ibtimes.tumblr.com' not in newLink):
                        self.scrape_analyze_store_article(newLink)
            except Exception as e:
                print(f'Error loading info from page {i}:', e)


    def find_articles_from_main_business_page(self, search_URL, numOfPages=1):
        """Finds all URLs from Business section's home page"""
        page = requests.get(search_URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll('a')
        linksToSave = []
        for link in links:
            newLink = link.get('href')
            if newLink.count('/') == 1 and newLink.count('-') > 1:
                linksToSave.append(newLink)
        linksToSave = list(set(linksToSave))
        for i in linksToSave:
            url = 'https://www.ibtimes.com' + i
            self.scrape_analyze_store_article(url)
        self.search_multiple_pages_business(search_URL, numOfPages)


    def search_multiple_pages_business(self, search_URL, numOfPages=1):
        """Finds all URLs by searching multiple pages from business section"""
        for i in range(1, numOfPages):
            try:
                URL = search_URL + f'?page={i}'
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, 'html.parser')
                links = soup.findAll('a')
                linksToSave = []
                for link in links:
                    newLink = link.get('href')
                    if newLink.count('/') == 1 and newLink.count('-') > 1:
                        linksToSave.append(newLink)
                linksToSave = list(set(linksToSave))
                for i in linksToSave:
                    url = 'https://www.ibtimes.com' + i
                    self.scrape_analyze_store_article(url)
            except Exception as e:
                print(e)

    def scrape_analyze_store_article(self, url):
        """Takes in a URL and sends it off to get extracted and saved"""
        try:
            web = Webscraper()
            article = web.scrape_article_from_web(url)
            article_sentiment_analysis = web.get_sentiment_analysis(article)
            web.print_dictionary(article_sentiment_analysis)
            web.add_row_to_saved_article_results_dataframe(article_sentiment_analysis)
        except Exception as e:
            print(e)