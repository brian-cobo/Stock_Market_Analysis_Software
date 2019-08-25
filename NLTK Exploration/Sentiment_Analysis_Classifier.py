import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split


# https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk


def predict_sentiment():
    data = pd.read_csv('train.tsv', sep='\t')
    token = RegexpTokenizer(r'[a-zA-Z0-9]+')

    cv = CountVectorizer(lowercase=True,
                         stop_words='english',
                         ngram_range=(1,1),
                         tokenizer=token.tokenize)
    text_counts = cv.fit_transform(data['Phrase'])


    X_train, X_test, y_train, y_test = train_test_split(text_counts,
                                                        data['Sentiment'],
                                                        test_size=0.2,
                                                        random_state=1)
    clf = MultinomialNB().fit(X_train, y_train)
    predicted = clf.predict(X_test)
    print("MultinomialNB Accuracy:",metrics.accuracy_score(y_test, predicted))

predict_sentiment()
