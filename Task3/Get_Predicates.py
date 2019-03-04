# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 12:17:33 2019

@author: Kaushikee
"""

''' libraries for predicate finding part '''
from SPARQLWrapper import SPARQLWrapper, JSON

    

predicate_forward = []
predicate_backward = []
predicate_forward_label = []
predicate_backward_label = []
predicate = []
    
#getting labels for the predicates
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
        


#Getting all the predicates for the entity    
def getPred(source):
    try:
        if '/page/' in str(source):
            source = source.replace('/page/','/resource/')
        query_forward = " PREFIX dbpedia: <" +source+"> SELECT distinct ?p WHERE { dbpedia: ?p ?o .}"
        
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setQuery(query_forward)
    
    
        sparql.setReturnFormat(JSON)
        results_forward = sparql.query().convert()
        
        for result in results_forward["results"]["bindings"]:
            
            if 'ontology' in str(result["p"]["value"]):
                if 'none' not in str(result["p"]["value"]):
                    predicate_forward.append(str(result["p"]["value"]))
                    predicate_forward_label.append(getLabel(str(result["p"]["value"])))
           
        
        query_backward = " PREFIX dbpedia: <" +source+"> SELECT distinct ?p WHERE { ?o ?p dbpedia: .}"
       
        sparql = SPARQLWrapper("http://dbpedia.org/sparql") 
        sparql.setQuery(query_backward)
    
    
        sparql.setReturnFormat(JSON)
        results_backward = sparql.query().convert() 
        
        for result in results_backward["results"]["bindings"]:
         
            if 'ontology' in str(result["p"]["value"]):
                if 'none' not in str(result["p"]["value"]):
                    predicate_backward.append(str(result["p"]["value"]))
                    predicate_backward_label.append(getLabel(str(result["p"]["value"])))
    
        return predicate_forward, predicate_backward, predicate_forward_label, predicate_backward_label
        
        
        
    except Exception as e:
        print("type error: " + str(e))       

