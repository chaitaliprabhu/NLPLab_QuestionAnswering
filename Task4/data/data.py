from gensim.corpora import Dictionary
import pandas as pd
import numpy as np
from pathlib import Path
import os

class Data:
    """
    class acts as a convenient data feeder for few shots learning
    """

    def __init__(self, datapath=None, seed=3, remove_unk=False):
        self.remove_unk = remove_unk
        np.random.seed(seed)
        # loading vocab
        current_file = Path().resolve().parent
        parent_of_parent_dir = os.path.join(current_file, '..\\')
        self.word_vocab = Dictionary.load_from_text(str(parent_of_parent_dir)+"\\Task4\\data\\word.vocab")
        self.entity_vocab = Dictionary.load_from_text(str(parent_of_parent_dir)+"\\Task4\\data\\entity.vocab")
        self.predicate_vocab = Dictionary.load_from_text(str(parent_of_parent_dir)+"\\Task4\\data\\predicate.vocab")
        # loading data files names
        self.datafile ="./data/final/train_output.txt"#, "valid": os.path.join(datapath, "valid.txt"),"test": os.path.join(datapath, "valid.txt")}
        self.data = {}

    def read_data(self):
        f = self.datafile
        x = pd.read_csv(f, names=["id", "question", "sub", "pred", "obj", "direction", "constraint" ],delimiter="\t", encoding="UTF-8")
        x.reset_index(inplace=True)
        temp = []
        for question in x['question']:
            question = "<s> " + question + " <\s>"
            temp.append(question)
        x['question'] = temp
        tmp = [[],[]]
        for l in x.iterrows():
            tmp[0].append([self.word_vocab.token2id[i] for i in l[1]['question'].split()])
            tmp[1].append(1 if (l[1]['direction']=="forward") else 2)
        x['direction'] =tmp[1]
        x['question'] = tmp[0]
        x['question_length'] = x.apply(lambda l: len(l['question']), axis=1)
        x['triple'] = x.apply(lambda l: [self.entity_vocab.token2id[l['sub']], self.predicate_vocab.token2id[l['pred']], self.entity_vocab.token2id[l['obj']]], axis=1)
        return x

    def datafeed(self, config, shuffle=True):
        """
        :param mode: train, valid, test
        :param config: config object
        :param shot_percentage: float between 0 and 1 indicating the percentage of the training data taken into consideration
        :param min_count: int indicating the minimum count of the predicates of the examples being taken in to consideration
        :param shuffle: whether to shuffle the training data or not
        :param kfold: a number between 1 and 10
        :return:
        """

        x = self.read_data() 
        self.data = x
        dataids = x.index
        y = self.yield_datafeed(dataids, x, config)
        print (y)
        return y
    
    def pad(self, x, pad_char=0, max_length=None):
        if max_length is None:
            max_length = max([len(i) for i in x])
                
        y = np.ones([len(x), max_length]) * pad_char
                
        for c, i in enumerate(x):
            y[c, :len(i)] = i
                        
        return y

    def yield_datafeed(self, dataids, x, config):
        
        """given a dataframe and selected ids and a mode yield data for experiments
        :param mode:
        :param dataids:
        :param x:
        :param config:
        :return:
        """

        for epoch in range(config.MAX_EPOCHS):

            def chunks(l, n):
                #Yield successive n-sized chunks from l.
                for i in range(0, len(l), n):
                    yield l[i:i + n]

            for bn, batchids in enumerate(chunks(dataids, config.BATCH_SIZE)):

                batch = x.iloc[batchids]
                yield (
                        np.array([i for i in batch['triple'].values]),
                        self.pad(batch['question'].values),
                        batch['question_length'].values,
                        batch['direction'].values,
                       {"epoch": epoch, "batch_id": bn, "ids": batchids}
                       )