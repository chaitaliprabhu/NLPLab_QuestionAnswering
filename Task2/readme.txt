This modules deals with detecting the direction and relation in the question and retrieving answer for the detected Entity and Relation by querying over DBpedia. Also, returning these answers as sentences.

Files and their content

train.h5: contains the questions and their direction for each predicate retrieved from the training file.
direction.joblib: contains the logistic regression model for the direction prediction.
predicates_values.txt: contains predicates and their corresponding sentence templates.

Scripts and their functions

quest_direction_train: retrieves all questions, predicates and respective directions from the training file.
train_direction:trains a logistic regression model for question direction predication.
question_processing: processes questions with POS tagging and returns the words that help in predicting the relation.
similarity: computes similarityy between relation from question and all other predicates for the entity from the DBpedia page.
answer_processing: retrieves answers from DBpedia.
question_answering: gets the templates for the relation and returns answers as sentences.  
