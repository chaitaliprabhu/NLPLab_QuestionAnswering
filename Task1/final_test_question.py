from __future__ import unicode_literals, print_function

import spacy, requests
from SPARQLWrapper import SPARQLWrapper, JSON
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english')) 

headers = {
    'Content-Type': 'application/json',
}

'''
Example 1) Question : Who was the director of Titanic?

Output:
Relation: director

Entity: Titanic
Link: http://dbpedia.org/page/Titanic_(1997_film)

Example 2) Question : Who is the spouse of Barack Obama?

Output:
Relation: spouse

Entity: Barack Obama
Link: http://dbpedia.org/page/Barack_Obama   
'''

def getLink(entity):
    try:
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.addDefaultGraph("http://dbpedia.org")
        sparql.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
               SELECT DISTINCT ?uri ?label
            WHERE {
            ?uri rdfs:label ?label .
            filter(?label="""+'"'+entity+'"'+"""@en)
            }
        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        if (results['results']['bindings'][0]['uri']['value']) == None:
            entity = entity
        r = requests.get(results['results']['bindings'][0]['uri']['value'])
        return r.url
    except Exception as e:
        print("type error: " + str(e))

def getRelation(query):
    data = '{"nlquery":'+query+', "pagerankflag": true}'
    word_relation = {}
    response = requests.post('http://sda.tech/earl/api/processQuery', headers=headers, data=data)
    word_list = response.json()['chunktext']
    for word in word_list:
        word_ = word['chunk']
        class_ = word['class']
        if class_ == 'relation':
            word_relation[word_] = class_
    for wrd, rel in word_relation.items():
        if rel == 'relation':
            return wrd


def getEARlentity(query):
    query = '"' +query + '"'
    data = '{"nlquery":'+query+', "pagerankflag": true}'
    response = requests.post('http://sda.tech/earl/api/processQuery', headers=headers, data=data)
    word_list = response.json()['chunktext']
    for word in word_list:
        word_ = word['chunk']
        class_ = word['class']
        if class_ == 'entity':
            earl_ent = word_
            return earl_ent
    
def getEntity(query, output_new_dir):
    ner_model = spacy.load(output_new_dir)
    doc = ner_model(query)
    if doc.ents:
        entity = [(ent.text) for ent in doc.ents][0]
        return entity
    else:
        return 'Entity not Detected'

def getEntity_Link(output_dir = "", question= ""):
    dbp_source = 'http://dbpedia.org/resource/'
    '''Question is stored in the below variable query'''
    query = '\"' + question + '\"'
    #Entity
    entity = getEntity(query[1:-2], output_dir)
    if entity == 'Entity not Detected':
        entity = getEARlentity(query[1:-2])  
    #DbPedia Link
    if len(entity.split()) == 1:
        link = dbp_source + entity.capitalize()
        request = requests.get(link)
        if request.status_code == 200:
            link = requests.get(link).url
        else:
            link = getLink(entity)
    else:
            link = getLink(entity)
        
    #Relation
    relation = getRelation(query)
    
    return entity, link, relation	