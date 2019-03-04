# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 00:52:30 2019

@author: Chaitali
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from joblib import dump, load

def train_save_direction_model(question = ""):
    
    store = pd.HDFStore('Task2/train.h5','r')
    df = store['df']
    store.close()
    
    x_train = df['question'].values
    y_train = df['direction'].values
    
    questions_train, questions_test, y_train, y_test = train_test_split(
        x_train, y_train, test_size=0.25, random_state=1000)
    
    vectorizer = CountVectorizer()
    vectorizer.fit(questions_train)
    X_train = vectorizer.transform(questions_train)
    #X_test  = vectorizer.transform(questions_test)
    
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    dump(classifier, 'Task2/direction.joblib') 
    #score = classifier.score(X_test, y_test)
    #print('Accuracy for ', score)
    classifier2 = load('Task2/direction.joblib')

    testList = []
    testList.append(question)
    pred = classifier2.predict(vectorizer.transform(testList))
    return pred

#if __name__ == "__main__":
#    train_save_direction_model("who is the spouse of Barack Obama?")
    