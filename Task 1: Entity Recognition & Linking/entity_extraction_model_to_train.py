from __future__ import unicode_literals, print_function

import random
from pathlib import Path
import spacy
from quepy import generateTrainingData
from tqdm import tqdm # loading bar

'''nlp1 = spacy.load('en')
docx1 = nlp1(u"Who was Kofi Annan?")
for token in docx1.ents:
    print(token.text,token.start_char, token.end_char,token.label_)
docx2 = nlp1(u"Who is Steve Jobs?")
for token in docx2.ents:
    print(token.text,token.start_char, token.end_char,token.label_)
docx3 = nlp1(u"Who is Shaka Khan?")'''
# training data
'''train_data = [
    ('What is Warner Bros?', {
        'entities': [(8, 19, 'ORG')]
    }),
    ('I like London and Berlin.', {
        'entities': [(7, 13, 'LOC'), (18, 24, 'LOC')]
    })
]'''
TRAIN_DATA = [('what movie is produced by warner bros ', {'entities': [(26, 37, 'Company')]}), ('what is don graham known as ', {'entities': [(8, 19, 'Person')]}), ("what 's there to see in columbus ", {'entities': [(24, 32, 'Place')]}), ('who is a musician born in detroit ', {'entities': [(26, 33, 'Place')]}), ('which city did the artist ryna originate in ', {'entities': [(26, 30, 'Agent')]}), ('who produced the film rough house rosie ', {'entities': [(22, 39, 'Film')]}), ('what is the language in which mera shikar was filmed in ', {'entities': [(30, 41, 'Film')]}), ('whats the name of a battle that happened in chicago ', {'entities': [(44, 51, 'Place')]}), ('which country is cheney tech in ', {'entities': [(-1, 34, 'School')]}), ('which red army general was involved in the great patriotic war ', {'entities': [(43, 63, 'GEN')]}), ('what is the position that mike twellman plays ', {'entities': [(26, 39, 'Person')]}), ('what is a name of gay night club in england ', {'entities': [(36, 43, 'MusicalArtist')]}), ('name a location in italy ', {'entities': [(19, 24, 'Person')]}), ("what is ellen swallow richards 's nationality ", {'entities': [(8, 30, 'Person')]}), ('name a city in nepal ', {'entities': [(15, 20, 'Place')]}), ('name a post punk artist ', {'entities': [(-1, 8, 'Genre')]}), ('what is an example of a private university ', {'entities': [(24, 42, 'University')]}), ('what is the gender of james hendry ', {'entities': [(22, 35, 'Person')]}), ('what is a school under the high school category ', {'entities': [(27, 38, 'School')]}), ('who did jean genet influence ', {'entities': [(8, 18, 'Person')]}), ('who was a voice actor ', {'entities': [(-1, 11, 'Person')]}), ('what is a mountain in the appalachian mountains ', {'entities': [(26, 47, 'Place')]}), ('what country utilizes the tomadino language ', {'entities': [(26, 43, 'Language')]}), ('in what automotive class is the hyundai santa fe ', {'entities': [(32, 48, 'Automobile')]}), ('name an album by serge gainsbourg ', {'entities': [(17, 33, 'Person')]}), ('what is a book by laura ingalls wilder ', {'entities': [(18, 38, 'Person')]}), ('what type of music fall heads roll ', {'entities': [(19, 34, 'Album')]}), ('who was the cinematographer for the film endless love ', {'entities': [(41, 54, 'Film')]}), ('what musical genre does brandon reilly create ', {'entities': [(24, 38, 'GEN')]}), ('whats a city in hungary ', {'entities': [(16, 23, 'Place')]}), ('where in germany was rudi ball born in ', {'entities': [(21, 30, 'Person')]}), ('what language comes from bodish languages ', {'entities': [(25, 41, 'Language')]}), ('what time zone is marrakech in ', {'entities': [(-1, 8, 'Place')]}), ('name a japanese action film ', {'entities': [(16, 27, 'MusicGenre')]}), ('which country does harry blackstone jr come from ', {'entities': [(19, 35, 'GEN')]}), ("what 's a place in central european time zone ", {'entities': [(19, 40, 'SportsEvent')]}), ('what movie did liliana cavani direct ', {'entities': [(15, 29, 'Person')]}), ('in what format was destroy the machines released ', {'entities': [(19, 39, 'Album')]}), ('what kind of video game is the dog island ', {'entities': [(27, 41, 'Software')]}), ('what television genre is the starter wife ', {'entities': [(25, 42, 'TelevisionShow')]}), ('who is an artist known for alternative hip hop ', {'entities': [(-1, 18, 'GEN')]}), ('where is the artist vitas from ', {'entities': [(20, 25, 'Person')]}), ('what did jane austen write ', {'entities': [(9, 20, 'Person')]}), ('what district is salempur uttar pradesh in ', {'entities': [(17, 25, 'Place')]}), ('what is the nationality of estella warren ', {'entities': [(27, 41, 'Person')]}), ('what type of reserve is the san juan national forest ', {'entities': [(28, 52, 'Place')]}), ('what is a film produced by the national film board of canada ', {'entities': [(31, 60, 'Agent')]}), ('is the golden age an album or dvd ', {'entities': [(3, 18, 'Album')]}), ('what gender does eugênio sales identify as ', {'entities': [(17, 30, 'Person')]}), ('name a person born in chicago ', {'entities': [(22, 29, 'Place')]}), ('what kind of music does john duffey play ', {'entities': [(24, 35, 'Person')]}), ('what tracks are by slinkeeminx ', {'entities': [(-1, 11, 'Agent')]}), ('who wrote the music for gangs of new york ', {'entities': [(24, 41, 'Film')]}), ('what is the gender of sophie merry ', {'entities': [(22, 34, 'Person')]}), ("what is moderat 's origin ", {'entities': [(8, 15, 'Agent')]}), ('what film story credits did louis n parker contribute to ', {'entities': [(28, 35, 'Person')]}), ('what genre of music is on the album get damned ', {'entities': [(36, 46, 'Album')]}), ('what kind of tv show is frontpage ', {'entities': [(24, 34, 'TelevisionShow')]}), ('what is an episode written by michelle ashford ', {'entities': [(30, 46, 'Person')]}), ('what is james g blaine most known for ', {'entities': [(8, 15, 'Person')]}), ('whats the name of a heavy metal artist ', {'entities': [(-1, 16, 'Genre')]}), ('what industry does aventurine sa participate in ', {'entities': [(19, 32, 'Company')]}), ('which is the main ideology of the communist party of britain ', {'entities': [(34, 60, 'Agent')]}), ('what album has folk music ', {'entities': [(15, 25, 'Genre')]}), ('who wrote the film thunderbolt and lightfoot ', {'entities': [(19, 44, 'Film')]}), ("what is imam mustafayev 's gender ", {'entities': [(8, 23, 'Person')]}), ('what is darren dods known for doing for a profession ', {'entities': [(8, 19, 'Person')]}), ('what type of music is robert roth known for ', {'entities': [(22, 34, 'Person')]}), ('who is the manufacturer of sikorsky hh 60 jayhawk ', {'entities': [(-1, 21, 'Aircraft')]}), ('what type of film is generation kill ', {'entities': [(21, 37, 'TelevisionShow')]}), ('which recording label is webbie with ', {'entities': [(25, 31, 'Person')]}), ('what is located in fort washington ', {'entities': [(19, 34, 'Place')]}), ('which country is john berry from ', {'entities': [(17, 28, 'Person')]}), ("what is joseph meyer 's job ", {'entities': [(8, 21, 'Person')]}), ('what kind of book is home ', {'entities': [(21, 26, 'Book')]}), ('what kinds of software is mldonkey ', {'entities': [(26, 34, 'Software')]}), ('what is the nationality of lorenzo maitani ', {'entities': [(27, 42, 'Person')]})]
#TRAIN_DATA = generateTrainingData()
#print(type(TRAIN_DATA))
TEST_DATA = ["Who is warner bros?", "I like london and berlin."]

# Define our variables
model = None
output_dir=Path("D:\\New folder\\NLP\\outputModel")
n_iter=100

if model is not None:
    nlp = spacy.load(model)  # load existing spaCy model
    print("Loaded model '%s'" % model)
else:
    nlp = spacy.blank('en')  # create blank Language class
    print("Created blank 'en' model")

# create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
if 'ner' not in nlp.pipe_names:
    ner = nlp.create_pipe('ner')
    nlp.add_pipe(ner, last=True)
# otherwise, get it so we can add labels
else:
    ner = nlp.get_pipe('ner')
    # add labels
for _, annotations in TRAIN_DATA:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])


'''for _, annotations in open('traindata.txt', 'r', encoding = 'utf-8'):
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])'''

    # get names of other pipes to disable them during training
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
with nlp.disable_pipes(*other_pipes):  # only train NER
    optimizer = nlp.begin_training()
    for itn in range(n_iter):
        random.shuffle(TRAIN_DATA)
        losses = {}
        for text, annotations in tqdm(TRAIN_DATA):
            nlp.update(
                [text],  # batch of texts
                [annotations],  # batch of annotations
                drop=0.5,  # dropout - make it harder to memorise data
                sgd=optimizer,  # callable to update weights
                losses=losses)
        print(losses)

# test the trained model
for text, _ in TRAIN_DATA:
    doc = nlp(text)
    print('Entities Train', [(ent.text, ent.label_) for ent in doc.ents])
    print('Tokens Train', [(t.text, t.ent_type_, t.ent_iob) for t in doc])

# save model to output directory
if output_dir is not None:
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to", output_dir)

# test the saved model
print("Loading from", output_dir)
nlp2 = spacy.load(output_dir)
for text, _ in TRAIN_DATA:
    doc = nlp2(text)
    print('Entities Test', [(ent.text, ent.label_) for ent in doc.ents])
    print('Tokens Test', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
