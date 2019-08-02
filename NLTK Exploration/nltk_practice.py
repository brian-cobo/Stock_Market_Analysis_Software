import pandas as pd
import numpy as np
import matplotlib as plt
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import RegexpTokenizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer

lem = WordNetLemmatizer()
ps = PorterStemmer()
tfidf_transformer = TfidfTransformer()


with open('Apple-Article.txt') as file:
    file = file.read()

tokenized_sentence = sent_tokenize(file)
tokenized_words = word_tokenize(file)
frequencyDist = FreqDist(tokenized_words).most_common(10)
stop_words=set(stopwords.words("english"))

# Filtering out stop words from the sentences
filtered_sent=[]
for w in tokenized_words:
    if w not in stop_words:
        filtered_sent.append(w)

#Printing out the stemmed versions of the words
stemmed_words=[]
for w in filtered_sent:
    stemmed_words.append(ps.stem(w))

# Printing the part of speech of the words i.e. verbs, nouns, ... etc
pos_words = nltk.pos_tag(tokenized_words)

# lemmatizing the words by using the part of speech
lemmatized_words = []
for word, pos in pos_words:
    try:
        if len(word) > 1:
            word = (word).lower()
            pos = ((pos).lower())[0]
            lemmatized_words.append(lem.lemmatize(word, pos))
    except Exception as e:
        pass


# print('Tokenized Sentence:', tokenized_sentence)
# print('Tokenized Words:', tokenized_words)
# print('Stop Words:', stop_words)
# print("Filtered Sentence:",filtered_sent)
# print("Stemmed Sentence:",stemmed_words)
# print('Lemmatized Words:', lemmatized_words)

