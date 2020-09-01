#Author: Ming Jeng
#Description:
#Code for the Actionable Item Extraction task; called by app.py
#Code uses sentence_classification model as first pass inference then uses email_intent_classification model as a second pass inference
#To bold any sentences that's highly likely to be actionable item
#Other Dependencies:
# models/cnn.h5
# models/cnn.json
from __future__ import print_function

import os
import sys

import numpy as np
import keras

from flask_model_helper import load_encoded_data
from flask_model_helper import encode_data, import_embedding, get_transcript_sentences, encode_transcript
from flask_model_helper import get_custom_test_comments

from keras.preprocessing import sequence
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D

from keras.preprocessing.text import Tokenizer
from nltk import word_tokenize

from email_inference import email_intent

import spacy
spacy_nlp = spacy.load("en_core_web_sm")

def inferencing(get_transcript,load_model_flag,model_name,dialogue_str):
#python3 sentence_cnn_save.py models/cnn path_to_transcript

    embedding_name = "data/default"
    # Model configuration
    maxlen = 500
    batch_size = 64
    embedding_dims = 75
    filters = 100
    kernel_size = 5
    hidden_dims = 350
    epochs = 2
        
        # Add parts-of-speech to data
    pos_tags_flag = True


    print('Loading model!')

    # load json and create model
    with keras.backend.get_session().graph.as_default():
        json_file = open(model_name + '.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        
        # load weights into new model
        model.load_weights(model_name + ".h5")
        print("Loaded model from disk")
        
        # evaluate loaded model on test data
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
    
        #CHECK if inputs and outputs are correct
        test_comments = get_transcript_sentences(dialogue_str)
        print('Number of input sentences:',len(test_comments))
        x_test = encode_transcript(test_comments,data_split=0,embedding_name=embedding_name,add_pos_tags_flag=pos_tags_flag)
        x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
        print('Transcript Inference')
        #PREDICT TIME and OUTPUTS
        predictions = model.predict(x_test, batch_size=batch_size, verbose=1)
        print('raw predictions:',predictions.shape)
        test = []
        for i in range(0, len(predictions)):
            test.append(predictions[i].argmax(axis=0))
        print('number of output sentences',len(test))
        
        #Getting what we want
        sorted_commands = []
        email_input = []
        for i in range(len(test)):
            label = ""
            spec = 0
            if test[i] == 1:
                label="QUESTION"
            elif test[i] == 2:
                label="STATEMENT"
            else:
                label = "COMMAND"
                if len(word_tokenize(test_comments[i])) < 3:
                    continue
                total_action_item = []
                front_context = " "
                back_context = " "
                if i>=2:
                    front_context+=test_comments[i-2]+'\n '+test_comments[i-1]
                if i< len(test_comments)-2:
                    back_context+=test_comments[i+1]+'\n '+test_comments[i+2]
                total_action_item.append(front_context)
                total_action_item.append(test_comments[i])
                total_action_item.append(back_context)
                #total_action_item+="\n"+str(float(predictions[i][3])*100)+"%"
                email_input.append(test_comments[i])
                #Check if there's date NER in sentence
                doc = spacy_nlp(test_comments[i])
                for ent in doc.ents:
                    if ent.label_ == "DATE" or ent.label_ == "TIME":
                        spec = 2
                        break
                sorted_commands.append([total_action_item,float('%.3f'%(float(predictions[i][3])*100)),spec])
       #Second Pass Inference: Uses Email Intent Classification model 
        email_predicted = email_intent(email_input)
        print('number of email predictions:', len(email_predicted))
        print('number of sentence classification predictions:',len(sorted_commands))
        for i in range(len(email_predicted)):
            if email_predicted[i][0] == 1:
                sorted_commands[i][2] = 1
        sorted_commands = sorted(sorted_commands,key=lambda x:(-x[1],x[0]))
        if len(sorted_commands) > 9:
            sorted_commands = sorted_commands[:6]
        return [[tup[0],"("+str(tup[1])+'%)',tup[2]] for tup in sorted_commands]
if __name__ == "__main__":
    
    inferencing(get_transcript,load_model_flag,model_name,dialogue_str)
