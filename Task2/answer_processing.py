# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 18:48:20 2019

@author: Chaitali
"""

from SPARQLWrapper import SPARQLWrapper, JSON
from Task2.similarity import get_Sim
from nltk.corpus import stopwords
from stop_words import get_stop_words
import numpy as np
from textblob import TextBlob

def getLabel(source):
    if source.find("/page/") != -1:
        source = source.replace("page", "resource")
    
    query = "PREFIX dbpedia: <" +source+">  PREFIX dbschema: <http://www.w3.org/2000/01/rdf-schema#>  SELECT DISTINCT ?label WHERE{ dbpedia: dbschema:label ?label FILTER (  lang(?label) = 'en') }"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    
    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        for result in results["results"]["bindings"]:
            return result["label"]["value"]
    except Exception as e:
        print("type error: " + str(e))

def getPredicateLabels(predicates):
    predDict = {}
    for predicate in predicates:
        predDict[getLabel(predicate)] = predicate
    return predDict

def getPredicates(link,direction):
    if link.find("/page/") != -1:
        link = link.replace("page", "resource")
    query = ""
    if direction=="forward":
        query = "PREFIX dbpedia: <" +link+"> SELECT DISTINCT ?predicate WHERE{ dbpedia: ?predicate ?object.  FILTER CONTAINS(STR(?predicate),'ontology')}"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    predicates = []
    
    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        for result in results["results"]["bindings"]:
            predicates.append(result["predicate"]["value"])
    except Exception as e:
        print("type error: " + str(e))
        
    return predicates

def getBestPredicate(predDict, ENTITY_OTHER):
    predicate = ""
    predicate_link = ""
    predicate = getSimilarityFromModel(predDict, ENTITY_OTHER)
    return predicate
    
def getAnswer(sub_Link, pred_Link, direction = ""):
    if sub_Link.find("/page/") != -1:
        sub_Link = sub_Link.replace("page", "resource")
    if pred_Link.find("/property/") != -1:
        pred_Link = pred_Link.replace("property", "ontology")
    query = ""
    if(direction == 'forward'):
        query = "PREFIX dbpedia: <" +sub_Link+">  PREFIX dbschema: <" +pred_Link+">  SELECT DISTINCT ?answer WHERE{ dbpedia: dbschema: ?answer.  }"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(query)
    answers = []
    answer_links = []
    
    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        
        for result in results["results"]["bindings"]:
            answer = result["answer"]["value"]
            if answer.find("/") != -1:
                if("/page/" in str(answer)):
                    answer = answer.replace("/page/","/resource/")
                answer_links.append(answer)
                answers.append(getLabel(answer))
            else:
                answers.append(answer)
            
    except Exception as e:
        print("type error: " + str(e))
    return answers,answer_links

def remove_stop_words(ENTITY_OTHER):
    stop_words = list(get_stop_words('en'))         #About 900 stopwords
    nltk_words = list(stopwords.words('english')) #About 150 stopwords
    stop_words.extend(nltk_words)

    output = [w for w in ENTITY_OTHER if not w in stop_words]
    #print("output ", output)
    return output

def getSimilarityFromModel(predDict, ENTITY_OTHER):
    similarities = []
    predList = []
    for pred in predDict:
        similarities.append(get_Sim(str(pred).lower(), str(ENTITY_OTHER).lower()))
        predList.append(pred)
    index_min = np.argmax(similarities)
    bestPredicate = str(predList[index_min])
    #print("pred " , bestPredicate)
    return bestPredicate

def getPluralForm(predicate):
    words = predicate.strip().split(" ")
    #print("Length ", len(words))
    blob = TextBlob(words[len(words) - 1])
    plurals = [word.pluralize() for word in blob.words]
    #print(plurals)
    words[len(words) - 1] = plurals
    plural_Str = ' '.join(str(e) for e in words)
    return plural_Str.replace("]","").replace("[","").replace("\'","")
