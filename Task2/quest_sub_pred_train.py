# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 18:55:04 2019

@author: Chaitali
"""

from SPARQLWrapper import SPARQLWrapper, JSON

import urllib
import json
import pandas as pd

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
df = pd.DataFrame(columns=['question', 'subj_Label', 'subj_Link', 'pred_Label', 'pred_Link'])
    
ent_Prefix = "http://dbpedia.org/resource/"
pred_Prefix = "http://dbpedia.org/ontology/"
data = json.loads(myfile)
questions = data['Questions']

i = 0
for item in questions:
    predicates = item['PredicateList']
    for predicate in predicates:
        question = item['Query']
        subject = item['Subject']
        pred = predicate['Predicate']
        
        subjLabelSearch = subject.split("/")[-1]
        predLabelSearch = pred.split("/")[-1]
        
        labelSearchLink = ent_Prefix+subjLabelSearch
        predLabelSearchLink = pred
        
        sub_Label = getLabel(labelSearchLink)
        pred_Label = getLabel(predLabelSearchLink)
        df.loc[i] = [question, sub_Label, subject, pred_Label, pred]
        i += 1
store = pd.HDFStore('Task2/questions.h5')
store['df'] = df 
