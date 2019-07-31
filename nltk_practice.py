
import nltk
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer


with open('Apple-Article.txt') as file:
    file = file.read()

tokenized_sentence = sent_tokenize(file)
print('Tokenized Sentence:', tokenized_sentence)

tokenized_words = word_tokenize(file)
print('Tokenized Words:', tokenized_words)

frequencyDist = FreqDist(tokenized_words).most_common(10)


stop_words=set(stopwords.words("english"))
print('Stop Words:', stop_words)

filtered_sent=[]
for w in tokenized_words:
    if w not in stop_words:
        filtered_sent.append(w)
#print("Tokenized Sentence:",tokenized_words)
#print("Filtered Sentence:",filtered_sent)


ps = PorterStemmer()

stemmed_words=[]
for w in filtered_sent:
    stemmed_words.append(ps.stem(w))

print("Filtered Sentence:",filtered_sent)
print("Stemmed Sentence:",stemmed_words)


lem = WordNetLemmatizer()
print(lem.lemmatize('flying', "v"))

print(nltk.pos_tag(tokenized_words))



