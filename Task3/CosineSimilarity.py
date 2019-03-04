# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:36:27 2019

@author: Kaushikee
"""

import spacy
'''Download spacy model en_core_web_md using below command:
    python -m spacy download en                 # for default English model (~50MB)
    python -m spacy download en_core_web_md     # for larger English model (~1GB) and comment line 7 & uncomment line 8
    '''
    

import numpy as np
import numpy.ma as ma
import scipy
from operator import itemgetter

def getCosineSimilarity(predicate, predicate_forward, predicate_backward, predicate_forward_label, predicate_backward_label):

# Load the spacy model that you have installed
    nlp = spacy.load('en')
    word_vec_list_forward = []
    word_vec_list_backward = []
    predicate_question = predicate
    
    #Get the list of predicates from the file
    #Convert the words from the predicate list into vectors
    for word in predicate_forward_label:
        if len(word or ()) != 0:
            doc = nlp(word)
        # Get the vector for 'words' and appending to a list:
            word_vec_list_forward.append(doc.vector)
    #saving the list of word vectors to a text file
    for word in predicate_backward_label:
        if len(word or ()) != 0:
            doc = nlp(word)
        # Get the vector for 'words' and appending to a list:
            word_vec_list_backward.append(doc.vector)    
            
    token = nlp(predicate_question)
    vector_form = token.vector

    a = np.array(vector_form)
    b_forward = np.array(word_vec_list_forward)
    b_backward = np.array(word_vec_list_backward)
    aa = a.reshape(1,-1)
    #bb = b.reshape(1,-1)
    distances_forward = scipy.spatial.distance.cdist(aa, b_forward, 'cosine')
    distances_backward = scipy.spatial.distance.cdist(aa, b_backward, 'cosine')
    dist_forward = distances_forward[0]
    dist_backward = distances_backward[0]

    minval_forward = np.min(ma.masked_where(dist_forward==0, dist_forward))
    minval_backward = np.min(ma.masked_where(dist_backward==0, dist_backward))
    
    
    if minval_forward<minval_backward:   
        index_min_forward = np.argmin(ma.masked_where(dist_forward==0, dist_forward))
        result_forward = itemgetter(index_min_forward)(predicate_forward)
        direction = 'forward'
        return result_forward, direction
    
    else:
        index_min_backward = np.argmin(ma.masked_where(dist_backward==0, dist_backward))
        result_backward = itemgetter(index_min_backward)(predicate_backward)
        direction = 'backward'
        return result_backward, direction