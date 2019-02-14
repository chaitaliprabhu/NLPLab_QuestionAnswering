# -*- coding: utf-8 -*-
"""
@author: maya_he
"""
import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer
from pathlib import Path

def evaluate(ner_model, examples):
    scorer = Scorer()
    for input_, annotations in examples:
        doc_gold_text = ner_model.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annotations.get('entities'))
        pred_value = ner_model(input_)
        scorer.score(pred_value, gold)
    return scorer.scores

# sample data - while running use data from testdata.txt
examples = [('which genre of album is harder faster ', {'entities': [(24, 31, 'Album')]}), ('what format is fearless ', {'entities': [(15, 24, 'Album')]})]
output_dir=Path("D:\\New folder\\NLP\\outputModel")
#ner_model_path = spacy.load(output_dir)
ner_model = spacy.load(output_dir) # for spaCy's pretrained use 'en_core_web_sm'
results = evaluate(ner_model, examples)
print(results)