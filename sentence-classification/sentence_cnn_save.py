'''
Written by Austin Walters
Last Edit: January 2, 2019
For use on austingwalters.com

A CNN to classify a sentence as one 
of the common sentance types:
Question, Statement, Command, Exclamation

Heavily Inspired by Keras Examples: 
https://github.com/keras-team/keras
'''

from __future__ import print_function

import os
import sys

import numpy as np
import keras

from sentence_types import load_encoded_data
from sentence_types import encode_data, import_embedding, get_transcript_sentences, encode_transcript
from sentence_types import get_custom_test_comments

from keras.preprocessing import sequence
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Activation, Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D

from keras.preprocessing.text import Tokenizer
from nltk import word_tokenize

import spacy
spacy_nlp = spacy.load("en")


#python3 sentence_cnn_save.py models/cnn path_to_transcript

if len(sys.argv) != 3:
    print("Wrong number of arguments, this warning forces you to do inferencing by loading model")
    exit()


get_transcript = False
dialogue_str = ""
#Read in transcript file
if len(sys.argv) > 2:
    file_name = sys.argv[2]
    f = open(file_name,"r")
    lines = f.readlines()
    for line in lines:
        dialogue_str+=line
    get_transcript = True

# Use can load a different model if desired
model_name      = "models/cnn"
embedding_name  = "data/default"
load_model_flag = False
arguments       = sys.argv[1:len(sys.argv)]
if len(arguments) >= 1:
    model_name = arguments[0]
    load_model_flag = os.path.isfile(model_name+".json")
print(model_name)
print("Load Model?", (load_model_flag))


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


if not load_model_flag:
        
    # Export & load embeddings
    x_train, x_test, y_train, y_test = load_encoded_data(data_split=0.8,
                                                         embedding_name=embedding_name,
                                                         pos_tags=pos_tags_flag)
    
    word_encoding, category_encoding = import_embedding(embedding_name)
    
    max_words   = len(word_encoding) + 1
    num_classes = np.max(y_train) + 1
    
    print(max_words, 'words')
    print(num_classes, 'classes')
    
    print('Pad sequences (samples x time)')
    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    
    print('Convert class vector to binary class matrix '
          '(for use with categorical_crossentropy)')
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)


    print('Constructing model!')

    model = Sequential()

    model.add(Embedding(max_words, embedding_dims,
                        input_length=maxlen))
    
    model.add(Dropout(0.2))
    
    model.add(Conv1D(filters, kernel_size, padding='valid',
                     activation='relu', strides=1))
    
    model.add(GlobalMaxPooling1D())
    
    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
    
    model.add(Dense(num_classes))
    model.add(Activation('softmax'))
    
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    
    model.fit(x_train, y_train, batch_size=batch_size,
              epochs=epochs, validation_data=(x_test, y_test))

    model_json = model.to_json()
    with open(model_name + ".json", "w+") as json_file:
        json_file.write(model_json)
    
    # serialize weights to HDF5
    model.save_weights(model_name + ".h5")
    print("Saved model to disk")

else:

    print('Loading model!')

    # load json and create model
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



#TEMPRORARILY COMMENT OUT THE TESTING EVALUATION 

#score = model.evaluate(x_test, y_test, batch_size=batch_size, verbose=1)
    
#print('Test accuracy:', score[1])

if get_transcript:
    test_comments = get_transcript_sentences(dialogue_str)
    print('Number of input sentences:',len(test_comments))
    x_test = encode_transcript(test_comments,data_split=0,embedding_name=embedding_name,add_pos_tags_flag=pos_tags_flag)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    print('Transcript Inference')
    predictions = model.predict(x_test, batch_size=batch_size, verbose=1)
    test = []
    for i in range(0, len(predictions)):
        test.append(predictions[i].argmax(axis=0))
    print('inference:', test)
    print('number of output sentences',len(test))
    for i in range(len(test)):
        label = ""
        if test[i] == 1:
            label="QUESTION"
            #print(i,label,test[i],test_comments[i])
        elif test[i] == 2:
            label="STATEMENT"
        else:
            label = "COMMAND"
            if len(word_tokenize(test_comments[i])) < 3:
                continue
            #doc = spacy_nlp(test_comments[i])
            #for ent in doc.ents:
                #if ent.label_ == "DATE":                  
            print(i,test_comments[i-1])
            print(i,label,test[i],test_comments[i])
            print(i,test_comments[i+1])
            print('-----------')
    output =  open('sentence-classification/senClass_predictions.txt','w+')
    print('Start overwriting previous predictions in .txt file')
    for p in test:
        output.write('%s\n' % p)
    output.close()
else:
    test_comments, test_comments_category = get_custom_test_comments()
    
    x_test, _, y_test, _ = encode_data(test_comments, test_comments_category,
                                       data_split=1.0,
                                       embedding_name=embedding_name,
                                       add_pos_tags_flag=pos_tags_flag)
    
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
    score = model.evaluate(x_test, y_test,
                           batch_size=batch_size, verbose=1)
    
    
    print('Manual test')
    print('Test accuracy:', score[1])
    
# Show predictions
    print(len(x_test))
    predictions = model.predict(x_test, batch_size=batch_size, verbose=1)

    real = []
    test = []
    for i in range(0, len(predictions)):
        real.append(y_test[i].argmax(axis=0))
        test.append(predictions[i].argmax(axis=0))

    print("Predictions")
    print("Real", real)
    print("Test", test)
