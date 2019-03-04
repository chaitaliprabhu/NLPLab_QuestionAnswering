# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 17:01:24 2018

@author: Chaitali
"""
import nltk
from nltk.stem.wordnet import WordNetLemmatizer

length_TaggedQuestion=0

def processQuestion_tags(question = ""):
    tokens = nltk.word_tokenize(question)
    #print("Question ", question)
    
    taggedQuestion = nltk.pos_tag(tokens)
    #print("POS " , taggedQuestion)
    return taggedQuestion

def processQuestion_verb(taggedQuestion = ""):
    length_TaggedQuestion = len(taggedQuestion) - 1
    VERB = ""
    first = True
    flag = False
    for i in range(0, length_TaggedQuestion):
        verb_true = (taggedQuestion [i][1][0] == 'V')
        if verb_true == True:
            if first == True:
                flag = True
                VERB = str (taggedQuestion [i][0])
                first = False
            else:
                flag = False
                VERB = VERB +" "+ (taggedQuestion [i][0])
    return VERB,flag

def processQuestion_other(taggedQuestion = "", VERB = ""):
    length_TaggedQuestion = len(taggedQuestion) - 1
    VERBS = VERB.split(" ")
    INFVERB = ""
    OTHERS = ""
    first = True
    lemmatizer = WordNetLemmatizer()
    for i in range(0, length_TaggedQuestion):
        wordtype = str(taggedQuestion [i][1])
        word = str(taggedQuestion [i][0])
        comNoun_true = (wordtype == 'NN' or (wordtype == 'NNS' and word[0].islower()) or wordtype == 'JJ')
        for verb in VERBS:
            if comNoun_true == True:
                INFVERB = lemmatizer.lemmatize(verb, 'v')
                if str(INFVERB) == "be" or str(INFVERB) == "have":
                        if first == True:
                            OTHERS = word
                            first = False
                        else:
                            OTHERS = OTHERS +" "+word
                else:
                    if first == True:
                        OTHERS = verb + " "+word
                        first = False
                    else:
                        OTHERS = OTHERS +" "+verb + " "+word
    return OTHERS

"""def isVerb(predicate):
    tokens = nltk.word_tokenize(predicate)
    taggedPred = nltk.pos_tag(tokens)
    print("tokens ", taggedPred[0][1])
    verb_true = (taggedPred[0][1][0] == 'V')
    return verb_true"""