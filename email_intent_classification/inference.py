
from keras.models import load_model
from keras.preprocessing import sequence
from nltk import pos_tag, word_tokenize, sent_tokenize, PorterStemmer
from nltk.corpus import stopwords
import sys
import csv
import pandas as pd
stop_w = stopwords.words('english')
# Read transcript file into a string
dialogue_str = ""
file_name = sys.argv[1]
f = open(file_name,"r")
lines = f.readlines()
for line in lines:
   dialogue_str+=line
dialogue_str = dialogue_str.strip()
dialogue_str = dialogue_str.replace("\n"," ")
sentences = sent_tokenize(dialogue_str)
if len(sentences) == 1:
    from deepsegment import DeepSegment
    segmenter=DeepSegment('en')
    sentences = segmenter.segment_long(sentences[0])
#Get Vocab Dictionary for tokenization in next step
with open('vocab.csv',mode = 'r') as infile:
    reader = csv.reader(infile)
    with open('vocab_new.csv',mode='w') as outfile:
        writer = csv.writer(outfile)
        word2idx = {rows[0]:rows[1] for rows in reader}
#print(word2idx)
#Encode all the tokenized sentences
total_tokenized = []
max_length = 0
ps = PorterStemmer()
for sentence in sentences:
    sent_tokens = []
    for word in word_tokenize(sentence):
        #word = word.lower()
        #stem = ps.stem(word)
        #if word in stop_w or stem in stop_w:
        #    print(word)
        #    continue
        if word not in word2idx:
            sent_tokens.append(1)
        else:
            sent_tokens.append(word2idx[word])
    if len(sent_tokens) > max_length:
        max_length = len(sent_tokens)
    total_tokenized.append(sent_tokens)

inference_input  = sequence.pad_sequences(total_tokenized, maxlen=100)

model = load_model('best_cnn_weights.hdf5')
model.summary()
predicted = model.predict_classes(inference_input)
print('Number of sentences input into the model', len(sentences))
print('model output number of sentences:', len(predicted))
for i in range(len(predicted)):
    if predicted[i][0] == 1:
        print('PREV SENT:',sentences[i-1])
        print('ACTION:',i,sentences[i])
        print('---------')
output = open("boxer_predictions.txt","w+")
for p in predicted:
    output.write('%s\n' % p[0])
output.close()

print('max tokens length sentence:',max_length)

def email_intent(sentences):
    with open('vocab.csv',mode = 'r') as infile:
        reader = csv.reader(infile)
        with open('vocab_new.csv',mode='w') as outfile:
            writer = csv.writer(outfile)
            word2idx = {rows[0]:rows[1] for rows in reader}
    #Encode all the tokenized sentences
    total_tokenized = []
    max_length = 0
    ps = PorterStemmer()
    for sentence in sentences:
        sent_tokens = []
        for word in word_tokenize(sentence):
            #word = word.lower()
            #stem = ps.stem(word)
            #if word in stop_w or stem in stop_w:
            #    print(word)
            #    continue
            if word not in word2idx:
                sent_tokens.append(1)
            else:
                sent_tokens.append(word2idx[word])
        if len(sent_tokens) > max_length:
            max_length = len(sent_tokens)
        total_tokenized.append(sent_tokens)

    inference_input  = sequence.pad_sequences(total_tokenized, maxlen=100)

    model = load_model('best_cnn_weights.hdf5')
    model.summary()
    predicted = model.predict_classes(inference_input)
    print('Number of sentences input into the email model', len(sentences))
    print('Email model output number of sentences:', len(predicted))
    for i in range(len(predicted)):
        if predicted[i][0] == 1:
            print('PREV SENT:',sentences[i-1])
            print('ACTION:',i,sentences[i])
            print('---------')
    return predicted
