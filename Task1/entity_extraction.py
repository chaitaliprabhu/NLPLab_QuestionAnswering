# -*- coding: utf-8 -*-
"""
Created on Sat Feb  2 12:14:03 2019

@author: maya_he
"""
from SPARQLWrapper import SPARQLWrapper, JSON
import spacy
#nlp = spacy.load('en') # install 'en' model (python3 -m spacy download en)
nlp = spacy.load('en_core_web_sm')

def getType(source):
    query_type = "PREFIX dbpedia: <" +source+">  PREFIX dbschema: <http://www.w3.org/2000/01/rdf-schema#>  SELECT DISTINCT ?type WHERE{ dbpedia: rdf:type ?type FILTER CONTAINS (str(?type), 'http://dbpedia.org/ontology')}"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_type)
    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            return result["type"]["value"].split('/')[-1]
    except Exception as e:
        print("type error: " + str(e))


def getLabel(source):
    query_label = "PREFIX dbpedia: <" +source+">  PREFIX dbschema: <http://www.w3.org/2000/01/rdf-schema#>  SELECT DISTINCT ?label WHERE{ dbpedia: dbschema:label ?label FILTER (  lang(?label) = 'en') }"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query_label)
    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        for result in results["results"]["bindings"]:
            return result["label"]["value"]
    except Exception as e:
        print("type error: " + str(e))

def getTuple(line):
    question = line.split("\t")[1]
    dbpedia_end_point = line.split("\t")[2]
    entity_label = getLabel(dbpedia_end_point)
    entity_type = getType(dbpedia_end_point)
    return question, entity_label, entity_type

def generateTrainingDataInstance(ques, ent_label, s_indx, e_indx, ent_type, ent_tuple_list):
    ent = {}
    ent['entities']= ent_tuple_list   
    training_pattern = (ques,ent)
    return training_pattern

def generateTrainingData():
    file_path = 'D:/New folder/NLP/inputs/test.txt'
    training_list = []
    for line in open(file_path, 'r', encoding = 'utf-8'):
        entity_tuple_list = []
        question, entity_label, entity_type  = getTuple(line)
        if entity_label:
            entity_label = entity_label.split('.')[0].split(',')[0].split('(')[0]
            if question.lower().find(entity_label.lower()):
                start_index = question.lower().find(entity_label.lower())
                end_index = start_index + len(entity_label.lower())
                entity_tuple_list = [(start_index, end_index, entity_type)]
                final_tuple = generateTrainingDataInstance(question, entity_label,start_index, end_index, entity_type, entity_tuple_list)
                training_list.append(final_tuple)
    return training_list, entity_label


if __name__ == "__main__":
    train_data = generateTrainingData()
    print(train_data)