# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 21:25:48 2019

@author: hemu
"""

import requests

headers = {
    'Content-Type': 'application/json',
}

def load_data(file_path):
    data = []
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            data.append(line)
        f.close()
    return data

def get_query(elem):
    if '\',' in elem:
        query = elem.split('\',')
    if '\",' in elem:
        query = elem.split('\",')
    query = query[0].strip()
    query = '\"' + query[2:] + '\"'
    return query

#Loading train and test data sets
train_data = load_data('train_data_new_sampe.txt')
test_data = load_data('test_data_new.txt')
word_relation = {}
word_rel_list = []
with open('entity_linking_output.txt', 'w', encoding = 'utf-8') as f:
    for elem in train_data:
        print(elem)
        query = get_query(elem)
        #print(query)
        f.write('\n')
        f.write(query)
        f.write('\n')
        data = '{"nlquery":'+query+', "pagerankflag": true}'
        #data = '{"nlquery":"what movie is produced by Warner Bros", "pagerankflag": true}'
        
        response = requests.post('http://sda.tech/earl/api/processQuery', headers=headers, data=data)
        #print(response.json())
        output = response.json()
        link_type = response.json()['ertypes']
        print('Question: ', query)
        print('Link Types :',link_type)
        word_list = response.json()['chunktext']
        for word in word_list:
            word_ = word['chunk']
            class_ = word['class']
            word_relation[word_] = class_
            #print(word_relation)
        word_rel_list.append(word_relation)        
        print('Word : Type ', word_rel_list)
        word_relation = {}
        word_rel_list = []
        f.write(str(response.json()))
        f.write('\n')