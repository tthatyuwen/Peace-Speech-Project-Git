import json
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import TextVectorization
import random
from sklearn.model_selection import train_test_split
from nltk.tokenize import word_tokenize
import gc
import pandas as pd

peace_country = ['Australia','Canada','Finland','France','Ireland','Norway','Singapore','UK']
oppo_country = ['Gambia','India','Iran','Ireland','Libya','Nigeria','Pakistan','Zimbabwe']
country_list = peace_country+oppo_country

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

def get_vocab(article_text_list,ngram=1,max_tokens=10000):
    text_vectorization = TextVectorization(ngrams=ngram,max_tokens = max_tokens,output_mode='multi_hot')
    article_ds = tf.data.Dataset.from_tensor_slices(article_text_list)
    text_vectorization.adapt(article_ds.batch(64))
    vocab = text_vectorization.get_vocabulary()
    return vocab 

def build_vector_layer(target_country_text,oppo_country_text,ngram=1,max_tokens=10000):
    target_vocab = get_vocab(target_country_text,ngram=ngram,max_tokens=max_tokens)
    oppo_vocab = get_vocab(oppo_country_text,ngram=ngram,max_tokens=max_tokens)
    vocab = list(set(target_vocab).intersection(set(oppo_vocab)))
    vocab.remove('[UNK]')
    text_vectorization = TextVectorization(ngrams=ngram,output_mode='multi_hot')
    text_vectorization.set_vocabulary(vocab)
    return text_vectorization

def unigram_logistic_model(max_tokens=10000,hidden_dim=32):
    inputs = keras.Input(shape=(max_tokens,))
    x = layers.Dropout(0.5)(inputs)
    outputs = layers.Dense(1,activation='sigmoid')(x)
    model = keras.Model(inputs,outputs)
    model.compile(optimizer='rmsprop',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def basemodel(target_country_name,ngram=1,max_tokens=10000,epoch=1,country_list_name=None):
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
    train_text, val_text, train_label, val_label = train_test_split(text_list, label, test_size = 0.5)
    train_text_ds = tf.data.Dataset.from_tensor_slices(train_text)
    train_ds = tf.data.Dataset.zip((train_text_ds, tf.data.Dataset.from_tensor_slices(train_label)))
    val_ds = tf.data.Dataset.zip((tf.data.Dataset.from_tensor_slices(val_text), tf.data.Dataset.from_tensor_slices(val_label)))
    text_vectorization = build_vector_layer(target_country_text,oppo_country_text,ngram=ngram,max_tokens=max_tokens)
    unigram_train_ds = train_ds.map(lambda x,y: (text_vectorization(x),y)).batch(64)
    unigram_val_ds = val_ds.map(lambda x,y: (text_vectorization(x),y)).batch(64)
    model = unigram_logistic_model(max_tokens=len(text_vectorization.get_vocabulary()))
    callbacks = [
        keras.callbacks.ModelCheckpoint('uninary_gram.keras',save_best_only=True)
    ]
    model.fit(unigram_train_ds.cache(),
                validation_data=unigram_val_ds.cache(),
                epochs=epoch,
                callbacks=callbacks)
    model = keras.models.load_model('uninary_gram.keras')
    return model,text_vectorization