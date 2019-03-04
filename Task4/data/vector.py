from gensim.corpora import Dictionary
import pandas as pd
f = "./final/test_output.txt"
x = pd.read_csv(f, names=["id", "question", "sub", "pred", "obj", "direction", "constraint"], delimiter="\t", encoding="UTF-8")
word_vocab = Dictionary.load_from_text("./word.vocab")
for q in x['question']: 
    word_vocab.add_documents([q.split()])
#word_vocab.save_as_text("word.vocab")
entity_vocab = Dictionary.load_from_text("./entity.vocab")
for s in x['sub']:
    entity_vocab.add_documents([s.split()])
for o in x['obj']:
    entity_vocab.add_documents([o.split()])
#entity_vocab.save_as_text("entity.vocab")
predicate_vocab = Dictionary.load_from_text("./predicate.vocab")
for p in x['pred']:
    predicate_vocab.add_documents([p.split()])
#predicate_vocab.save_as_text("predicate.vocab")
direction_vocab = Dictionary.load_from_text("./direction.vocab")
for d in x['direction']:
    direction_vocab.add_documents([d.split()])
direction_vocab.save_as_text("direction.vocab")
print("Done")




from gensim.corpora import Dictionary
import pandas as pd
f = "./final/train_output.txt"
g = "./final/test_output.txt"
x = pd.read_csv(f, names=["id", "question", "sub", "pred", "obj", "direction", "constraint"], delimiter="\t", encoding="UTF-8")
y = pd.read_csv(f, names=["id", "question", "sub", "pred", "obj", "direction", "constraint"], delimiter="\t", encoding="UTF-8")
word_vocab = Dictionary([['<UNK>','<s>','<\s>']])
for q in x['question']: 
    word_vocab.add_documents([q.split()])
for q in y['question']:
    word_vocab.add_documents([q.split()])
word_vocab.save_as_text("word.vocab")
print("Done")






