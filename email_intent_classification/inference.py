
from keras.models import load_model
from keras.preprocessing import sequence
from nltk import pos_tag, word_tokenize, sent_tokenize
import sys
import csv
import pandas as pd
# test = pd.read_csv('./resources/testing-cleaned.txt', sep='^', header=None)
dialogue_str = ""
file_name = sys.argv[1]
f = open(file_name,"r")
lines = f.readlines()
for line in lines:
   dialogue_str+=line

sentences = sent_tokenize(dialogue_str)
#Get Vocab Dictionary
with open('vocab.csv',mode = 'r') as infile:
    reader = csv.reader(infile)
    with open('vocab_new.csv',mode='w') as outfile:
        writer = csv.writer(outfile)
        word2idx = {rows[0]:rows[1] for rows in reader}
print(word2idx)
#Tokenize all the sentences
total_tokenized = []
max_length = 0
for sentence in sentences:
    sent_tokens = []
    for word in word_tokenize(sentence):
        if word not in word2idx:
            sent_tokens.append(1)
        else:
            sent_tokens.append(word2idx[word])
    if len(sent_tokens) > max_length:
        max_length = len(sent_tokens)
    total_tokenized.append(sent_tokens)

print('max tokens length sentence:',max_length)
inference_input  = sequence.pad_sequences(total_tokenized, maxlen=100)
print(inference_input)
model = load_model('best_cnn_weights.hdf5')
model.summary()
predicted = model.predict_classes(inference_input)

print('predicted:',predicted)

for i in range(len(predicted)):
    if predicted[i][0] == 1:
        print('PREV SENT:',sentences[i-1])
        print('ACTION:',sentences[i])
        print('---------')
# testData = test.as_numpy()
# xTest = 
# max_len = 0
# word2idx ={'UNK':1}
# currentIdx = 2
# xPreprocess = []
# for x in xTrain:
#     tokens = word_tokenize(x)
#     if len(tokens) > max_len:
#             max_len = len(tokens)
#         for t in tokens:
#             if t not in word2idx:
#                 word2idx[t] = currentIdx
#                 currentIdx += 1
#         sentences = [word2idx[w] for w in tokens]
#         xPreprocess.append(sentences)

#     xPreprocessTest = []
#     for xTest in xTest:
#         tokensTest = word_tokenize(xTest)
#         sentence = []
#         for tTest in tokensTest:
#             if tTest not in word2idx:
#                 sentence.append(1)
#             else:
#                 sentence.append(word2idx[tTest])
#         xPreprocessTest.append(sentence)

