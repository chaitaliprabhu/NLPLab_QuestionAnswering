# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 14:30:41 2019

@author: Chaitali
"""
from SPARQLWrapper import SPARQLWrapper, JSON

import urllib
import json

def getLabel(source):
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
    
link = "https://raw.githubusercontent.com/castorini/SimpleDBpediaQA/master/V1/train.json"
f = urllib.request.urlopen(link)
myfile = f.read()
    
pred_Prefix = "http://dbpedia.org/ontology/"
data = json.loads(myfile)
questions = data['Questions']
predicates_List = []
i = 0
f_write = open('predicates_values.txt', 'w+')
for item in questions:
    predicates = item['PredicateList']
    for predicate in predicates:
        pred = predicate['Predicate']
        predLabelSearch = pred.split("/")[-1]
        
        predLabelSearchLink = pred
        predLabelSearchLink = pred_Prefix+predLabelSearch
        
        pred_Label = getLabel(predLabelSearchLink)
        
        try:
            pred_Label = getLabel(predLabelSearchLink)
            if pred_Label != None:
                if str(pred_Label) not in predicates_List:
                    predicates_List.append(str(pred_Label))
        except:
            pass
for p in predicates_List:
    f_write.write(p)
    f_write.write("\n")   
f_write.close

with open('dbpedia-predicates.txt', 'r') as f:
    f_write = open('predicates_values.txt', 'w+')
    lines = f.readlines()
    for line in lines:
        try:
            label = getLabel(str(line).replace("\n",""))
            if label != None:
                if str(label) not in predicates_List:
                    predicates_List.append(str(label))
        except:
            pass
for p in predicates_List:   
    try:
        f_write.write(p)
        f_write.write("\n")
    except:
        pass
f_write.close
f.close
print(predicates_List)