# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 19:37:03 2019

@author: Chaitali
"""
from Task2.question_processing import processQuestion_tags, processQuestion_verb, processQuestion_other
from Task2.answer_processing import getPredicates, getPredicateLabels, getBestPredicate, getAnswer, getPluralForm
from Task2.train_direction import train_save_direction_model

def getRelation_and_Answer(question = "", noun = "", sub_Link= ""):

    direction = train_save_direction_model(question)
    #print("Direction = ", direction)
    if(direction == 'backward'):
        exit("Not generating answers for backward questions!")
    taggedQuestion = processQuestion_tags(question)
    #print("Noun = ", noun)
    
    ENTITY_VERB, flag  = processQuestion_verb(taggedQuestion)
    #print("Verb ", ENTITY_VERB)
    
    ENTITY_OTHER = processQuestion_other(taggedQuestion, ENTITY_VERB)
    #print("Other ", ENTITY_OTHER)
    
    if ENTITY_OTHER == "" or ENTITY_OTHER == None:
        ENTITY_OTHER = ENTITY_VERB
    else:
        ENTITY_OTHER = ENTITY_OTHER + " " + ENTITY_VERB
    
    if noun.strip() == "" or (ENTITY_OTHER.strip() == "" and flag == True):
        exit("Question is not framed correctly. Try again !")

    predicates = getPredicates(sub_Link,direction)
    if len(predicates) == 0:
        exit("No data in this link")
    predDict = getPredicateLabels(predicates)
    #print(predDict)
    
    bestPredicate = getBestPredicate(predDict, ENTITY_OTHER)
    if bestPredicate == None or bestPredicate.strip() == "":
        exit("No relation close to question")
    #print(predDict[bestPredicate])
    answers, answer_links = getAnswer(sub_Link, predDict[bestPredicate],direction)
    if len(answers) == 0:
        exit("No answer for the question")
    
    answerSentence = ""
    with open('Task2/predicates_values.txt', 'r', encoding = 'UTF-8',errors='ignore') as f:
        lines = f.readlines()
        for line in lines:
            try:
                values = line.rsplit(',',1)
                if str(bestPredicate).lower() == str(values[0]).lower():
                    answerSentence = str(values[1])
            except:
                pass
        f.close
    if answerSentence == "":
        answerSentence = "The Z of X is Y."
    ans_str = str(answers).replace("]","").replace("[","").replace("\'","")
    if len(answers) > 1:
            bestPredicate = getPluralForm(bestPredicate)
            if ' is ' in answerSentence:
                answerSentence = answerSentence.replace(' is ', ' are ')
    if 'X' in answerSentence:
        answerSentence = answerSentence.replace('X', noun)
    if 'Y' in answerSentence:
        answerSentence = answerSentence.replace('Y', ans_str)
    if 'Z' in answerSentence:
        answerSentence = answerSentence.replace('Z', bestPredicate)
    
    #print("Answer = ", answerSentence)
    return direction, bestPredicate, predDict[bestPredicate], answerSentence, answer_links
