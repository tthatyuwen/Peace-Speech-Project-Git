import json
import nltk
from nltk import pos_tag, word_tokenize
import country_converter_ as coco
import string
import pandas as pd
import regex as re

def text_cleaner(country):
    with open(f'./Data_Raw/{country}.json','r') as f:
        country_dict = json.load(f)
        text_list = pd.DataFrame(country_dict)['text']
        text_list = [text.encode('ascii','ignore').decode() for text in text_list]                        # remove ascii
        text_list = [text.translate(str.maketrans('','',string.punctuation)) for text in text_list]       # remove punctuation
    country_dict=[]
    for i in range(len(text_list)):
        country_dict.append({'text':text_list[i]})
    with open(f'./Data_First_Cleaned/{country}.json','w') as f:
        json.dump(country_dict,f)

def word_cleaner(country):
    with open(f'./Data_First_Cleaned/{country}.json','r') as f:
        country_dict = json.load(f)
    with open(f'./nltk_stopwords.txt','r') as f:
        stopwords = f.read().split(',')
    text_list = pd.DataFrame(country_dict)['text']
    word_array = [nltk.word_tokenize(text) for text in text_list]
    word_array = [[word for word in word_list if len(word)>2]for word_list in word_array]                               # remove words too short
    word_array = [[word for word,tag in pos_tag(word_list) if tag not in ['NNP','NNPS']] for word_list in word_array]   # remove propernoun
    word_array = [[word for word in word_list if word not in stopwords] for word_list in word_array]                    # remove stopwords in nltk
    text_list = [' '.join(word_list) for word_list in word_array]
    text_list = [text.lower() for text in text_list]                                                                    # lowercase
    test_list = [re.sub(r"[0-9]+",'',text) for text in text_list]                                                       # remove numbers
    _, text_list = coco.convert(text_list, src='regex', to='iso2')                                                      # remove countrys using coco
    country_dict=[]
    for i in range(len(text_list)):
        country_dict.append({'text':text_list[i]})
    with open(f'./Data_Cleaned/{country}.json','w') as f:
        json.dump(country_dict,f)

def clean_stopwords(country):                                                                                           # remove stopwords found in model
    with open('./stopwords.txt','r') as f:
        stopwords = f.read().split(',')
    with open(f'./Data_Cleaned/{country}.json','r') as f:
        country_dict = json.load(f)
    text_list = pd.DataFrame(country_dict)['text']
    words_list = [word_tokenize(text) for text in text_list]
    words_list = [[word for word in word_list if word not in stopwords] for word_list in words_list]
    text_list = [' '.join(word_list) for word_list in words_list]
    country_dict = []
    for i in range(len(text_list)):
        country_dict.append({'text':text_list[i]})
    with open(f'./Data_Final/{country}.json','w') as f:
        json.dump(country_dict,f)