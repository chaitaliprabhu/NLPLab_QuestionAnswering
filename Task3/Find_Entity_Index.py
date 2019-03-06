# -*- coding: utf-8 -*-


"""
Created on Sat Jan 12 00:33:45 2019

@author: Kaushikee
"""

''' libraries for entity rank part  '''
import os 
#finding the entity which has the highest index value
def getEntityRank(word1, word2):           
    
    word_value1 = word1.split('/')[-1]
    word_value2 = word2.split('/')[-1]
    current_file = os.getcwd()
    directoryPath= current_file+'/Task3/Entity_ranks'
    os.chdir(directoryPath)
   
    list_ent = []
    for folders, sub_folders, file in os.walk(directoryPath):
        for file in file:
            if file.endswith(".txt"):
                f = open(file, "r", encoding = 'utf-8')
                for l in f.readlines():
                    value = l.replace("[","").replace("]","").replace("\'","")
                    valueStr1 = value.split(",")
                    if len(valueStr1)==2:    
                        if((word_value1 == (valueStr1[0].strip())) or (word_value2 == (valueStr1[0].strip()))):
                            list_ent.append((valueStr1[0].strip(), valueStr1[1].strip()))
                    f.close()
    list_ent = list(set(list_ent))
    print("List ", list_ent)
    for item in list_ent:
        if item[0] == word_value2:
            ent_rank1 = item[1]
        if item[0] == word_value1:
            ent_rank2 = item[1]
    if ent_rank1>ent_rank2:
        entity_selected = word1
        if "/page/" in entity_selected:
            entity_selected = entity_selected.replace("/page/","/resource/")
        return entity_selected
    else:
        entity_selected = word2
        if "/page/" in entity_selected:
            entity_selected = entity_selected.replace("/page/","/resource/")
        return entity_selected   
