from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from Main_Program.Stock_Visualizations_Menu import search_for_company_symbol
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import string
import re
from Main_Program import Load_MasterDictionary as LM

MASTER_DICTIONARY_FILE = 'LoughranMcDonald_MasterDictionary_2018.csv'
lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, True)

# http://www.nltk.org/howto/sentiment.html
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
#https://sraf.nd.edu

#TODO
# Analyze company earnings reports
#       Twitter Example
#       https://www.nasdaq.com/aspx/stockmarketnewsstoryprint.aspx?storyid=twitter-announces-second-quarter-2019-results-20190726-00186


class Webscraper:
    def add_row_to_saved_article_results_dataframe(self, article_info):
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
        article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
        if os.path.exists(article_result_file_path):
            saved_article_results = pd.read_csv(article_result_file_path)
            if len(saved_article_results) > 0:
                return saved_article_results
            else:
                return self.create_saved_article_results_dataframe()
        return self.create_saved_article_results_dataframe()


    def check_for_existing_article_results(self, URL_to_check_for):
        article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
        if os.path.exists(article_result_file_path):
            article = pd.read_csv(article_result_file_path)
            data = article[(article.URL == URL_to_check_for)]
            if len(data) > 0:
                return True
            else:
                return False
        return False


    def filter_out_stop_words(self, tokenized_words):
        stop_words = set(stopwords.words("english"))
        filtered_sentence= []
        for word in tokenized_words:
            if word not in stop_words \
                    and (word.isalnum() == True
                         or word == '.'):
                filtered_sentence.append(word)
        filtered_sentence = (' ').join(filtered_sentence)
        return filtered_sentence

    def prepare_article(self):
        filePath = os.getcwd() + '/Articles/Apple-Article.txt'
        with open(filePath) as file:
            file = file.read()
        tokenized_sentence = sent_tokenize(file)
        return tokenized_sentence

    def get_sentiment_analysis(self, article_info):
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
        return soup.find_all('title')[0].get_text()

    def find_author_from_article(self, soup):
        return soup.find_all('span', itemprop='name')[0].get_text()

    def find_publish_date_and_time_from_article(self, soup):
        # Find Article Date and Time
        time = soup.find_all('time', itemprop='datePublished')
        published_time = ''
        for i in time:
            published_time += i.get_text()
        published_time = published_time.split()
        date_published = published_time[0]
        time_published = (' ').join(published_time[2:4])
        return (date_published, time_published)

    def find_article_content(self, soup):
        tag = soup.find_all('p')
        article = ''
        for i in tag:
            article += (i.get_text())
        return [article]

    def find_company_symbol_from_article(self, soup, title, article_content):
        # Find the Company Symbol the article talks about
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
        print()
        for key, value in dict.items():
            print(key, ':', value)

    def scrape_article_from_web(self, article_URL):
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
    def find_search_URL(self, string_to_search_for):
        search = string_to_search_for.replace(' ', '%20')
        search_URL = 'https://www.ibtimes.com/search/site/' + search
        print(search_URL)
        return search_URL

    def find_article_from_search_URL(self, search_URL, numPages=1):
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
        try:
            web = Webscraper()
            article = web.scrape_article_from_web(url)
            article_sentiment_analysis = web.get_sentiment_analysis(article)
            web.print_dictionary(article_sentiment_analysis)
            web.add_row_to_saved_article_results_dataframe(article_sentiment_analysis)
        except Exception as e:
            print(e)

def parser(doc):
    # 1. Number of words(based on LM_MasterDictionary
    # 2. Proportion of positive words(use with care - see LM, JAR 2016)
    # 3.  Proportion of negative words
    # 4.  Proportion of uncertainty words
    # 5.  Proportion of litigious words
    # 6.  Proportion of modal-weak words
    # 7.  Proportion of modal-moderate words
    # 8.  Proportion of modal-strong words
    # 9.  Proportion of constraining words (see Bodnaruk, Loughran and McDonald, JFQA 2015)
    # 10.  Number of alphanumeric characters (a-z, A-Z)
    # 11.  Number of digits (0-9)
    # 12.  Number of numbers (collections of digits)
    # 13.  Average number of syllables
    # 14.  Average word length
    # 15.  Vocabulary (see Loughran-McDonald, JF, 2015)


    doc = doc.upper()  # for this parse caps aren't informative so shift
    output_data = get_article_data(doc)
    article_info = {
        'numberOfWords': output_data[2],
        'positive_%': output_data[3],
        'negative_%': output_data[4],
        'uncertainty_%': output_data[5],
        'litigious': output_data[6],
        'modal-weak_%': output_data[7],
        'modal-moderate_%': output_data[8],
        'modal-strong_%': output_data[9],
        'constraining_%': output_data[10],
        'num_of_alphanumeric': output_data[11],
        'num_of_digits': output_data[12],
        'num_of_Numbers': output_data[13],
        'avg_num_Of_syllables_per_word': output_data[14],
        'avg_word_length': output_data[15],
        'vocabulary': output_data[16]
    }

    return article_info


def get_article_data(doc):
    vdictionary = {}
    _odata = [0] * 17
    total_syllables = 0
    word_length = 0

    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].positive: _odata[3] += 1
            if lm_dictionary[token].negative: _odata[4] += 1
            if lm_dictionary[token].uncertainty: _odata[5] += 1
            if lm_dictionary[token].litigious: _odata[6] += 1
            if lm_dictionary[token].weak_modal: _odata[7] += 1
            if lm_dictionary[token].moderate_modal: _odata[8] += 1
            if lm_dictionary[token].strong_modal: _odata[9] += 1
            if lm_dictionary[token].constraining: _odata[10] += 1
            total_syllables += lm_dictionary[token].syllables

    _odata[11] = len(re.findall('[A-Z]', doc))
    _odata[12] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[13] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))
    _odata[14] = total_syllables / _odata[2]
    _odata[15] = word_length / _odata[2]
    _odata[16] = len(vdictionary)

    # Convert counts to %
    for i in range(3, 10 + 1):
        _odata[i] = (_odata[i] / _odata[2]) * 100

    return _odata

if __name__ == "__main__":
    choice = 0
    print('Article Scraper/Sentiment Analysis')
    scraper = Find_Articles()
    while choice != -1:
        choice = int(input('\nChoose Option:\n'
                            '1: Retrieve Articles About Specific Company\n'
                            '2: Retrieve Articles From Front Page\n'
                            '-1: Quit\n'))
        if choice == -1:
            print('\nGoodbye\n')

        elif choice == 1:
            print('In choice 1')
            company = input("\nWhat company would you like to search articles for?\n")
            num_of_pages_to_search = int(input("\nHow many pages would you like to go through?\n"))
            scraper.find_article_from_search_URL(scraper.find_search_URL(company), num_of_pages_to_search)
        elif choice == 2:
            print('in choice 2')
            home_page_URL = f'https://www.ibtimes.com/business'
            num_of_pages_to_search = int(input("\nHow many pages would you like to go through?\n"))
            scraper.find_articles_from_main_business_page(home_page_URL,
                                                  num_of_pages_to_search)
        else:
            print('Choice not recognized')