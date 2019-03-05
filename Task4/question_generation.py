import tensorflow as tf

from Task4.config import Config
from Task4.data.data import Data
from Task4.triples2seq import Triple2SeqModel
from gensim.corpora import Dictionary
import numpy as np
from pathlib import Path
import os

def getSuggestiveQuestions(subject,predicate,obj_link,direction):

###########################
# Loading Data And Config #
###########################

    data = Data()
    config = Config(data)

###########
# testing #
###########
# loading back the trained model

    tf.reset_default_graph()
    model = Triple2SeqModel(config, 'inference')
    predicted_ids = []
    with tf.Session() as sess:
    #if tf.train.checkpoint_exists(tf.train.latest_checkpoint('../checkpoints/')):
        print('reloading the trained model')
        current_file = Path().resolve()
        parent_of_parent_dir = os.path.join(current_file, '../../')
        word_vocab = Dictionary.load_from_text(str(parent_of_parent_dir)+"/Task4/data/word.vocab")
        entity_vocab = Dictionary.load_from_text(str(parent_of_parent_dir)+"/Task4/data/entity.vocab")
        predicate_vocab = Dictionary.load_from_text(str(parent_of_parent_dir)+"/Task4/data/predicate.vocab")
        model.restore(sess=sess, path=tf.train.latest_checkpoint(str(parent_of_parent_dir)+"/Task4/checkpoints"))
        
        try:
            sub = entity_vocab.token2id[subject]
            pred = predicate_vocab.token2id[predicate]
            obj = entity_vocab.token2id[obj_link[0]]
       
            encoder_triples_inputs = np.array([[sub,pred,obj]])
            
            if (direction=="forward"):
                encoder_predicates_direction = [1]
            else:
                encoder_predicates_direction = [2]
        
            predicted_question =""
            predicted_ids = model.predict(sess, encoder_triples_inputs=encoder_triples_inputs, encoder_predicates_direction=encoder_predicates_direction)
       
            for i in range(len(predicted_ids[0])):
                x = predicted_ids[0,i]
                if (x.item(0) == 1):
                    break
                predicted_question = predicted_question + word_vocab[x.item(0)] + " "
            predicted_question = predicted_question + "?"
            return str(predicted_question)
        except Exception:
             return "Entity or Predicate out of vocabulary"

