from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from Stock_Visualizations_Menu import search_for_company_symbol
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import re
# http://www.nltk.org/howto/sentiment.html
# https://www.dataquest.io/blog/web-scraping-tutorial-python/

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
                                              'Overall_SA': article_info['Overall_SA'],
                                              'Positive_SA': article_info['Positive_SA'],
                                              'Negative_SA': article_info['Negative_SA'],
                                              'Neutral_SA': article_info['Neutral_SA']
                                             },
                                             ignore_index=True)
            self.clean_article_results_columns(article_results_dataframe)
        else:
            if self.check_for_null_values(article_info) == False:
                print('\nNot all values were found correctly, not saving:', article_info['URL'])
            else:
                print('\nArticle Info Already Saved')

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
                   'Date_Published', 'Time_Published', 'Overall_SA',
                   'Positive_SA', 'Negative_SA', 'Neutral_SA']
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
                                        'Overall_SA',
                                        'Positive_SA',
                                        'Negative_SA',
                                        'Neutral_SA'])
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
        article = article_info['Article']
        sid = SentimentIntensityAnalyzer()
        total_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
        average_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
        number_of_sentences = len(article)

        for sentence in article:
            results = sid.polarity_scores(sentence)
            total_sentiment_values['Compound'] += results['compound']
            total_sentiment_values['Positive'] += results['pos']
            total_sentiment_values['Negative'] += results['neg']
            total_sentiment_values['Neutral'] += results['neu']

        average_sentiment_values['Compound'] = float(total_sentiment_values['Compound'] / number_of_sentences)
        average_sentiment_values['Positive'] = float(total_sentiment_values['Positive'] / number_of_sentences)
        average_sentiment_values['Negative'] = float(total_sentiment_values['Negative'] / number_of_sentences)
        average_sentiment_values['Neutral'] = float(total_sentiment_values['Neutral'] / number_of_sentences)

        article_info['Overall_SA'] = average_sentiment_values['Compound']
        article_info['Positive_SA'] = average_sentiment_values['Positive']
        article_info['Negative_SA'] = average_sentiment_values['Negative']
        article_info['Neutral_SA'] = average_sentiment_values['Neutral']
        article_info.pop('Article', None)

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
                        print("ERROR:", e)
                break
        return company_symbol

    def print_dictionary(self, dict):
        for key, value in dict.items():
            print(key, ':', value)
        print()

    def scrape_article_from_web(self, article_URL):
        try:
            page = requests.get(article_URL)
            soup = BeautifulSoup(page.content, 'html.parser')
            #print(soup.prettify())

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


def main(url):
    try:
        web = Webscraper()
        article = web.scrape_article_from_web(url)
        article_sentiment_analysis = web.get_sentiment_analysis(article)
        web.print_dictionary(article_sentiment_analysis)
        web.add_row_to_saved_article_results_dataframe(article_sentiment_analysis)
    except Exception as e:
        print(e)


def find_search_URL(string_to_search_for):
    search = string_to_search_for.replace(' ', '%20')
    search_URL = 'https://www.ibtimes.com/search/site/' + search
    print(search_URL)
    return search_URL

def find_article_from_search_URL(search_URL, numPages):
    page = requests.get(search_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    links = soup.findAll('a', attrs={'href': re.compile("^https://")})
    for link in links:
        newLink = link.get('href')
        if ('twitter.com' not in newLink and
            'facebook.com' not in newLink and
            'linkedin.com' not in newLink and
            'ibtimes.tumblr.com' not in newLink):
            main(newLink)

    search_multiple_pages(search_URL, numPages)

def search_multiple_pages(search_URL, num_of_pages):
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
                    main(newLink)
        except Exception as e:
            print(f'Error loading info from page {i}:', e)



def find_articles_from_main_business_page(search_URL, numOfPages):
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
        main(url)
    search_multiple_pages_business(search_URL, numOfPages)


def search_multiple_pages_business(search_URL, numOfPages):
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
                main(url)
        except Exception as e:
            print(e)


home_page_URL=f'https://www.ibtimes.com/business'
#find_articles_from_main_business_page(home_page_URL, 20)
#find_articles_from_main_business_page(url2)
find_article_from_search_URL( find_search_URL('tesla'), 50)
