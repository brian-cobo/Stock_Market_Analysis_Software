from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfTransformer
from Stock_Visualizations_Menu import search_for_company_symbol
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from collections import Counter
import re
# http://www.nltk.org/howto/sentiment.html
# https://www.dataquest.io/blog/web-scraping-tutorial-python/


def add_row_to_saved_article_results_dataframe(article_info):
    if check_for_existing_article_results(article_info['URL']) == False:
        article_results_dataframe = return_article_results_dataframe()
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
        clean_article_results_columns(article_results_dataframe)
    else:
        print('\nArticle Info Already Saved')
        #article_results_dataframe = pd.read_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
        #clean_article_results_columns(article_results_dataframe)


def clean_article_results_columns(article_results_dataframe):
    columns = ['URL', 'Title', 'Company_Symbol', 'Author',
               'Date_Published', 'Time_Published', 'Overall_SA',
               'Positive_SA', 'Negative_SA', 'Neutral_SA']
    for column in article_results_dataframe.columns:
        if column not in columns:
            article_results_dataframe = article_results_dataframe.drop(columns=[column], axis=1)
            article_results_dataframe.to_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
    article_results_dataframe.to_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
    return article_results_dataframe

def create_saved_article_results_dataframe():
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

def return_article_results_dataframe():
    article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
    if os.path.exists(article_result_file_path):
        saved_article_results = pd.read_csv(article_result_file_path)
        if len(saved_article_results) > 0:
            return saved_article_results
        else:
            return create_saved_article_results_dataframe()
    return create_saved_article_results_dataframe()


def check_for_existing_article_results(URL_to_check_for):
    article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
    if os.path.exists(article_result_file_path):
        article = pd.read_csv(article_result_file_path)
        data = article[(article.URL == URL_to_check_for)]
        if len(data) > 0:
            return True
        else:
            return False
    return False


def filter_out_stop_words(tokenized_words):
    stop_words = set(stopwords.words("english"))
    filtered_sentence= []
    for word in tokenized_words:
        if word not in stop_words \
                and (word.isalnum() == True
                     or word == '.'):
            filtered_sentence.append(word)
    filtered_sentence = (' ').join(filtered_sentence)
    return filtered_sentence


def prepare_article():
    filePath = os.getcwd() + '/Articles/Apple-Article.txt'
    with open(filePath) as file:
        file = file.read()

    filtered_sentence = filter_out_stop_words(word_tokenize(file))

    #tokenized_sentence = sent_tokenize(filtered_sentence)
    tokenized_sentence = sent_tokenize(file)

    return tokenized_sentence

def get_sentiment_analysis(article_info):
    article = article_info['Article']
    sid = SentimentIntensityAnalyzer()
    total_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
    average_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
    number_of_sentences = len(article)

    for sentence in article:
        results = sid.polarity_scores(sentence)
        # print('Overall:', results['compound'],
        #       ' Positive:', results['pos'],
        #       ' Negative:', results['neg'],
        #       ' Neutral:', results['neu'])
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

def find_title_from_article(soup):
    return soup.find_all('title')[0].get_text()

def find_author_from_article(soup):
    return soup.find_all('span', itemprop='name')[0].get_text()

def find_publish_date_and_time_from_article(soup):
    # Find Article Date and Time
    time = soup.find_all('time', itemprop='datePublished')
    published_time = ''
    for i in time:
        published_time += i.get_text()
    published_time = published_time.split()
    date_published = published_time[0]
    time_published = (' ').join(published_time[2:4])
    return (date_published, time_published)

def find_article_content(soup):
    tag = soup.find_all('p')
    article = ''
    for i in tag:
        article += (i.get_text())
    return [article]

def find_company_symbol_from_article(soup, title, article_content):
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
                    symbols = search_for_company_symbol(key, automated=True)
                    if (key in title.lower() and
                            key in article_content[0].lower() and
                            key in symbols.Name.iloc[0].lower()):
                        company_symbol = symbols.Symbol.iloc[0]
                        break
                except Exception as e:
                    print("ERROR:", e)
            break
    return company_symbol

def print_dictionary(dict):
    for key, value in dict.items():
        print(key, ':', value)
    print()

def scrape_article_from_web(article_URL):
    page = requests.get(article_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())

    title = find_title_from_article(soup)
    author = find_author_from_article(soup)
    date_published, time_published = find_publish_date_and_time_from_article(soup)
    article_content = find_article_content(soup)
    company_symbol = find_company_symbol_from_article(soup, title, article_content)

    article_extracted_info = {'URL' : article_URL,
                              'Title' : title,
                              'Company_Symbol': company_symbol,
                              'Author': author,
                              'Date_Published' : date_published,
                              'Time_Published' : time_published,
                              'Article' : article_content}


    return(article_extracted_info)


url1 = 'https://www.ibtimes.com/apple-stock-4-q3-earnings-beat-despite-low-iphone-sales-2809781?ft=2gh92&utm_source=Robinhood&utm_medium=Site&utm_campaign=Partnerships'
url2 = 'https://www.ibtimes.com/does-starbucks-want-become-tech-company-2810671'
url3 = 'https://www.ibtimes.com/tesla-news-elon-musks-company-faces-lawsuit-over-fatal-florida-autopilot-crash-2810583'
url4 = 'https://www.ibtimes.com/which-walmart-stores-are-closing-2019-full-list-locations-2796471'

#Create a function to replace spaces with %20 and that will serve as automated searching for articles
search_results_for_apple_url ='https://www.ibtimes.com/search/site/apple'
search_results_for_apple_url_2 = 'https://www.ibtimes.com/search/site/apple%20inc'


def main(url):
    article = scrape_article_from_web(url)
    article_sentiment_analysis = get_sentiment_analysis(article)
    print_dictionary(article_sentiment_analysis)
    add_row_to_saved_article_results_dataframe(article_sentiment_analysis)

main(url1)
main(url2)
main(url3)
main(url4)




