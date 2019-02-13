# Entity Recognition & Linking:

'entity_extraction.py': Here SPARQL queries for DBpedia are written for getting the entity labels and the type of the entity and data preprocessing is done on the 'train.txt' file and extracted the entities. 
'entity_extraction_model_to_train.py': In this file the extracted entities are trained using the spacy over the train_data_sample.txt which is obtained after the data pre-processing.
'entity_extraction_model_to_train_File.py': An updated version with mini-batches that made the code run very fastly
