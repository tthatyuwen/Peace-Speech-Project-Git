from unigram import *
import copy
import numpy as np

def keywords(country):
    sub_country_list,sub_peace_country = copy.deepcopy(country_list),copy.deepcopy(peace_country)
    sub_country_list.remove(country)
    if country in sub_peace_country:
        sub_peace_country.remove(country)
    model,text_vectorization = basemodel(sub_peace_country,max_tokens=10000,ngram=1,country_list_name=sub_country_list)
    weight = model.layers[2].weights[0].numpy()
    target_index = np.argsort(-weight,axis=0)[:300].reshape(-1)
    oppo_index = np.argsort(weight,axis=0)[:300].reshape(-1)
    vocabulary = text_vectorization.get_vocabulary()
    positive_words = ','.join([vocabulary[i] for i in target_index])
    negative_words = ','.join([vocabulary[i] for i in oppo_index])
    with open(f'./keywords/positive/{country}.txt','w') as f:
        f.write(positive_words)
    with open(f'./keywords/negative/{country}.txt','w') as f:
        f.write(negative_words)

def keywords_common():
    positive_words,negative_words = [],[]
    for country in country_list:
        with open(f'./keywords/positive/{country}.txt','r') as f:
            pos_words = f.read().split(',')
        positive_words.extend(pos_words)
        with open(f'./keywords/negative/{country}.txt','r') as f:
            neg_words = f.read().split(',')
        negative_words.extend(neg_words)
    pos = [words for words in set(positive_words) if positive_words.count(words)==len(country_list)]
    neg = [words for words in set(negative_words) if negative_words.count(words)==len(country_list)]
    return pos,neg

if __name__ == '__main__':
    for country in country_list:
        keywords(country)
    pos,neg = keywords_common()
    print('pos:',pos)
    print('neg:',neg)