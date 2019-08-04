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

def check_for_existing_article_results(URL_to_check_for):
    article_result_file_path = os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv'
    if os.path.exists(article_result_file_path):
        article = pd.read_csv(article_result_file_path)
        data = article[(article.URL == URL_to_check_for)]
        if len(data) > 0:
            return data
        else:
            return None

    else:
        article = pd.DataFrame(columns=['URL',
                                        'Title',
                                        'Company',
                                        'Author',
                                        'Date',
                                        'Time',
                                        'Overall',
                                        'Positive',
                                        'Negative',
                                        'Neutral'])
        article.to_csv(os.getcwd() + '/Article_Sentiment_Results/Sentiment_Results.csv')
        return None

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

def get_sentiment_analysis():
    if check_for_existing_article_results() == None:
        print('Article Already Exists')
        exit(0)
    else:
        article = os.getcwd() + '/Articles/Apple-Article.txt'

    print('\nScores are rated from -1 (Highly Negative) to 1 (Highly Positive)')
    sid = SentimentIntensityAnalyzer()
    total_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
    average_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
    number_of_sentences = len(article)

    for sentence in article:
        print('\nSentence:', sentence)
        results = sid.polarity_scores(sentence)
        # print('Overall:', results['compound'],
        #       ' Positive:', results['pos'],
        #       ' Negative:', results['neg'],
        #       ' Neutral:', results['neu'])
        total_sentiment_values['Compound'] += results ['compound']
        total_sentiment_values['Positive'] += results['pos']
        total_sentiment_values['Negative'] += results['neg']
        total_sentiment_values['Neutral'] += results['neu']

    average_sentiment_values['Compound'] = float(total_sentiment_values['Compound'] / number_of_sentences)
    average_sentiment_values['Positive'] = float(total_sentiment_values['Positive'] / number_of_sentences)
    average_sentiment_values['Negative'] = float(total_sentiment_values['Negative'] / number_of_sentences)
    average_sentiment_values['Neutral'] = float(total_sentiment_values['Neutral'] / number_of_sentences)

    print('\nArticle Results:'
          ' Overall:', average_sentiment_values['Compound'],
          ' Positive:', average_sentiment_values['Positive'],
          ' Negative:', average_sentiment_values['Negative'],
          ' Neutral:', average_sentiment_values['Neutral'])

# Currently only works for IBTimes.com articles
def scrape_article_from_web(article_URL):
    page = requests.get(article_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())
    #Company


    # Find Article Title
    title = soup.find_all('title')[0].get_text()

    #Find Author
    author = soup.find_all('span', itemprop='name')[0].get_text() #property='article:author'

    # Find Article Date and Time
    time = soup.find_all('time', itemprop='datePublished')
    published_time = ''
    for i in time:
        published_time += i.get_text()
    published_time = published_time.split()
    date_published = published_time[0]
    time_published = (' ').join(published_time[2:4])

    # Find Article Content
    tag = soup.find_all('p')
    article = ''
    for i in tag:
        article += (i.get_text())
    article = [article]

    # Find the Company Symbol the article talks about
    company_symbol = ''
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
                            key in article[0].lower() and
                            key in symbols.Name.iloc[0].lower()):
                        company_symbol = symbols.Symbol.iloc[0]
                    break
                except Exception as e:
                    print("ERROR:", e)
            break

    article_extracted_info = {'Title' : title,
                              'Author': author,
                              'Date_Published' : date_published,
                              'Time_Published' : time_published,
                              'Symbol' : company_symbol,
                              'URL' : article_URL,
                              'Article' : article}
    print()
    for key, value in article_extracted_info.items():
        print(key, ':', value)
    return(article_extracted_info)


url = 'https://www.ibtimes.com/apple-stock-4-q3-earnings-beat-despite-low-iphone-sales-2809781?ft=2gh92&utm_source=Robinhood&utm_medium=Site&utm_campaign=Partnerships'
scrape_article_from_web(url)
#get_sentiment_analysis()

