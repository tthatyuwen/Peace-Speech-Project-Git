import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import random
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import gc
import pandas as pd
from sklearn.linear_model import LogisticRegression

peace_country = ['Australia','Canada','Finland','France','Ireland','Norway','Singapore','UK']
oppo_country = ['Gambia','India','Iran','Uganda','Libya','Nigeria','Pakistan','Zimbabwe']
country_list = peace_country+oppo_country
with open('./stopwords.txt','r') as f:
    stopwords = f.read().split(',')

def load_country_data(country):
    with open(f'./Data_Final/{country}.json','r') as f:
        data = json.load(f)
    text_list = [dicts['text'] for dicts in data]
    return text_list

def get_country_list_dict(country_list):
    country_dict = {}
    for country in country_list:
        country_dict[country] = load_country_data(country)
    return country_dict

def get_vocab(article_text_list,max_tokens=10000):
    text_vectorization = TfidfVectorizer(max_features=max_tokens,stop_words=stopwords)
    text_vectorization.fit(article_text_list)
    vocab = text_vectorization.vocabulary_
    return vocab 

def build_vector_layer(target_country_text,oppo_country_text,max_tokens=10000):
    target_vocab = get_vocab(target_country_text,max_tokens=max_tokens)
    oppo_vocab = get_vocab(oppo_country_text,max_tokens=max_tokens)
    vocab = list(set(target_vocab).intersection(set(oppo_vocab)))
    text_vectorization = TfidfVectorizer(vocabulary=vocab)
    return text_vectorization

def basemodel(target_country_name,ngram=1,max_tokens=10000,country_list_name=None):
    country_dict = get_country_list_dict(country_list_name)
    target_country_text = []
    oppo_country_text = []
    for country_name, country_text_list in country_dict.items():
        if country_name in target_country_name:
            target_country_text.extend(country_text_list)
        else:
             oppo_country_text.extend(country_text_list)
    sample_size = min(len(target_country_text),len(oppo_country_text))
    target_country_text,oppo_country_text = random.sample(target_country_text,sample_size),random.sample(oppo_country_text,sample_size)
    text_list = target_country_text+oppo_country_text
    label = [1 if i<len(target_country_text) else 0 for i in range(2*len(target_country_text))]
    # train_text, val_text, train_label, val_label = train_test_split(text_list, label, test_size = 0.5)
    train_text,train_label = text_list, label
    text_vectorization = build_vector_layer(target_country_text,oppo_country_text,max_tokens=max_tokens)
    train_matrix = text_vectorization.fit_transform(train_text)
    # val_matrix = text_vectorization.transform(val_text)
    lm = LogisticRegression(max_iter=1000).fit(X=train_matrix,y=train_label)
    # y_pred = lm.predict(val_matrix)
    return lm,text_vectorization