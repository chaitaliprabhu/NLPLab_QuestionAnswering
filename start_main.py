# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 14:36:58 2019

@author: Chaitali
"""
import os
from Task1.final_test_question import getEntity_Link
from Task2.question_answering import getRelation_and_Answer
from Task4.question_generation import getSuggestiveQuestions
from Task2.answer_processing import getAnswer

import nltk
nltk.download('averaged_perceptron_tagger')

from Task3.Find_Entity_Index import getEntityRank
from Task3.Get_Predicates import getPred
from Task3.CosineSimilarity import getCosineSimilarity

def start(question = ''):
    global ans
    global ques
    current_file = os.getcwd()
    output_dir = current_file+ "\\outputModel"
    
    #Module 1 = Entity Recognition and Entity Linking
    entity_name, entity_link, relation = getEntity_Link(output_dir, question)
    print("name = ", entity_name)
    print("link = ", entity_link)
    print("relation = ", relation)
    
    #Module 2 = Relation Recognition, Direction and Answer Generation
    direction, predicate, predicate_link, answer, answer_links = getRelation_and_Answer(question, entity_name, entity_link)
    print("direction = ", direction)
    print("predicate = ", predicate)
    print("predicate_link = ", predicate_link)
    print("answer = ", answer)
    print("answer_links = ", answer_links)
    ans = answer
    
    #Module 3 = Semantic Coherence Calculation
    singleitem = answer_links[-1]
    highest_entity_rank = getEntityRank(entity_link, singleitem)
    print ("maximum index is for entity =  ", highest_entity_rank)
    predicate_forward, predicate_backward, predicate_forward_label, predicate_backward_label = getPred(highest_entity_rank)
    NewPred, DirectionPred = getCosineSimilarity(predicate, predicate_forward, predicate_backward, predicate_forward_label, predicate_backward_label)
    print ("closest new resultant predicate = ",NewPred)
    print ("direction of new predicate is = ",DirectionPred)
   
    #Module 4 = Suggestive Question Generation
    object_label, object_link = getAnswer(highest_entity_rank, NewPred, DirectionPred)
    suggestiveQuestion = getSuggestiveQuestions(highest_entity_rank, NewPred, object_link, DirectionPred)
    print("Suggestive Question = " + suggestiveQuestion)
    ques = suggestiveQuestion
    
def getAnswerStr():
    global ans
    return ans

def getQues():
    global ques
    return ques
