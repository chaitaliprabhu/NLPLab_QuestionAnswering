
import argparse
import tensorflow as tf

from config import Config
from data.data import *
from models.triples2seq import Triple2SeqModel

parser = argparse.ArgumentParser(description='running experiments of question generation')
parser.add_argument('-datapath', '--datapath', help='path to the preprocessed data folder', required=True)
parser.add_argument('-min', '--mincount', help='int indicating the minimum count of the predicates of the examples being taken in to consideration', required=False)
parser.add_argument('-fold', '--fold', help='fold number', required=False)
parser.add_argument('-epochs', '--epochs', help='epochs', required=False)

args = parser.parse_args()

######################
# creating model name#
######################

model_name = "triples"

if args.fold is None:
    fold = 0
else:
    fold = int(args.fold)


###########################
# Loading Data And Config #
###########################

data = Data(datapath=args.datapath)
config = Config(data, model_name)

if args.epochs is not None:
    config.MAX_EPOCHS = int(args.epochs)

traindatafeed = data.datafeed(config)

###################
#  START TRAINING #
###################
tf.reset_default_graph()
model = Triple2SeqModel(config)
#model = Triple2SeqModel(config) 

print ("Start Training model %s " % model_name)
print ("\n-----------------------\n")

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    print('reloading the trained model')
    model.restore(sess=sess, path=tf.train.latest_checkpoint('./checkpoints/triples'))
    iterator = traindatafeed

    for d in iterator:
        
        encoder_triples_inputs, decoder_inputs, decoder_inputs_lengths, direction, meta = d
            
        loss = model.train(sess, encoder_triples_inputs, decoder_inputs, decoder_inputs_lengths, direction)
          
        if model.global_step.eval() % config.LOG_FREQUENCY == 0:
            print("Global Step %s Epoch %s  Batch %s \t Loss = %s" % (model.global_step.eval(), meta["epoch"], meta["batch_id"], np.mean(loss)))

        # Save the model checkpoint
        if model.global_step.eval() % config.SAVE_FREQUENCY == 0:
            print('Saving the model..')
            checkpoint_path = os.path.join(config.CHECKPOINTS_PATH)
            path = model.save(sess, checkpoint_path, global_step=model.global_step)
            