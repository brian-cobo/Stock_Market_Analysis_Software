from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfTransformer

# http://www.nltk.org/howto/sentiment.html

def prepare_article():
    stop_words = set(stopwords.words("english"))
    with open('Apple-Article.txt') as file:
        file = file.read()
    tokenized_sentence = sent_tokenize(file)
    print(tokenized_sentence)
    return tokenized_sentence

def get_sentiment_analysis():
    article = prepare_article()

    print('\nScores are rated from -1 (Highly Negative) to 1 (Highly Positive)')
    sid = SentimentIntensityAnalyzer()
    total_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
    average_sentiment_values = {'Compound': 0, 'Positive': 0, 'Negative': 0, 'Neutral': 0}
    number_of_sentences = len(article)

    for sentence in article:
        print('\nSentence:', sentence)
        results = sid.polarity_scores(sentence)
        print('\nOverall:', results['compound'],
              ' Positive:', results['pos'],
              ' Negative:', results['neg'],
              ' Neutral:', results['neu'])
        total_sentiment_values['Compound'] += results ['compound']
        total_sentiment_values['Positive'] += results['pos']
        total_sentiment_values['Negative'] += results['neg']
        total_sentiment_values['Neutral'] += results['neu']

    average_sentiment_values['Compound'] = float(total_sentiment_values['Compound'] / number_of_sentences)
    average_sentiment_values['Positive'] = float(total_sentiment_values['Positive'] / number_of_sentences)
    average_sentiment_values['Negative'] = float(total_sentiment_values['Negative'] / number_of_sentences)
    average_sentiment_values['Neutral'] = float(total_sentiment_values['Neutral'] / number_of_sentences)

    print('\n\n\nOverall for the article:\n', average_sentiment_values)




get_sentiment_analysis()

