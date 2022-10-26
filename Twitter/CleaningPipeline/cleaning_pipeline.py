import pandas as pd
import country_converter_ as coco
import regex as re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import demoji
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import unicodedata

countries = {'IN': 'India', 'IR': 'Iran', 'NG': 'Nigeria', 'UG': 'Uganda',
             'GM': 'Gambia', 'LY': 'Libya', 'PK': 'Pakistan', 'ZW': 'Zimbabwe',
             'CA': 'Canada', 'GB': 'United Kingdom', 'FI': 'Finland', 'NO': 'Norway',
             'IE': 'Ireland', 'FR': 'France', 'AU': 'Australia', 'SG': 'Singapore'}

source = '<YOUR SOURCE OF INFORMATION HERE>'
data = pd.read_csv(source, lineterminator='\n')
regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
text = [re.sub(regex, '', i.lower()) for i in data['text']]
text = [unicodedata.normalize('NFKC', i) for i in text]
contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i will",
    "i'll've": "i will have",
    "i'm": "i am",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there would",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we would",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you would",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}
for i in range(len(text)):
    for word in text[i].split():
        if word.lower() in contractions:
            text[i] = text[i].replace(word, contractions[word])
    emoj = demoji.findall(text[i])
    for j in emoj:
        if 'flag' in emoj[j]:
            emoj[j] = emoj[j].replace('flag', ' ')
        text[i] = text[i].replace(j, ' '+emoj[j]+' ')

lemmatizer = WordNetLemmatizer()
word_list = [nltk.word_tokenize(i.lower()) for i in text]
text = [' '.join([lemmatizer.lemmatize(w) for w in i]) for i in word_list]

# Remove country names
loc, text_ = coco.convert(text, src='regex', to='iso2')

text_ = [' '.join([w for w in i.split() if len(w) > 2 and not w.isdigit() and '...' not in w]) for i in text_]

data['text_'] = text_
data['mentioned_country'] = loc
data['mentioned_country'] = data['mentioned_country'].replace('not found', '')

join_text = data.groupby(['country_code'])['text_'].apply(' '.join).reset_index()

text_total = [' '.join(join_text['text_'])]

# Get NLTK stopwords
stop_word = stopwords.words('english')

# Remove low frequency words
count_word = CountVectorizer(stop_words=stop_word)
total_word = count_word.fit_transform(text_total).toarray()[0]
vocab = count_word.vocabulary_
reverse_vocab = {v: k for k, v in vocab.items()}
ind = np.where(total_word == 1)[0]
remove_vocab = [reverse_vocab.get(i) for i in ind]

# Remove top N most unique words in each country
N = 100  # Set your own threshold here
counts = CountVectorizer(stop_words=stop_word+remove_vocab)
tf = counts.fit_transform(join_text['text_']).toarray()
X_total = np.sum(tf, axis=1)
tf = tf/X_total[:, None]
idf = np.array([np.array([1 if j > 0 else 0 for j in i]) for i in tf])
D_total = np.sum(idf, axis=0)
idf = np.log(len(idf)/D_total)
tfidf = tf*idf
vocab = counts.vocabulary_
reverse_vocab = {v: k for k, v in vocab.items()}
feature_names = counts.get_feature_names_out()
idx = tfidf.argsort(axis=1)
tfidf_max10 = idx[:, -N:]
tfidf_max10 = [i[::-1] for i in tfidf_max10]
top_10 = [[reverse_vocab.get(item) for item in row if item in reverse_vocab] for row in tfidf_max10]
top = pd.DataFrame(top_10)
top.index = [countries[i] for i in join_text['country_code']]
top = top.transpose()
final_list = []
for i in top_10:
    final_list += list(i)

# Compile NLTK stopwords, low frequency words, unique country words as final stopwords
stop_words = set(final_list+stop_word+remove_vocab)