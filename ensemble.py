import sys
from nltk import word_tokenize, sent_tokenize
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
    print('no punctuations')
    from deepsegment import DeepSegment
    segmenter=DeepSegment('en')
    sentences = segmenter.segment_long(sentences[0])
print('number of sentences:', len(sentences))
boxer_predictions = []
sentClass_predictions = []
with open('email_intent_classification/boxer_predictions.txt','r') as box:
    boxer = box.readlines()
    for line in boxer:
        boxer_predictions.append(line[:-1])
print('boxer predictions length:', len(boxer_predictions))
with open('sentence-classification/senClass_predictions.txt','r') as sen:
    s_lines = sen.readlines()
    for s in s_lines:
        sentClass_predictions.append(s[:-1])
print('sentence classification length:,',len(sentClass_predictions))
if len(boxer_predictions) != len(sentClass_predictions):
    raise Exception("There's unequal length in prediction outputs from the two model")
overlap = 0 
box_p = 0
senC_p =0
for i in range(len(boxer_predictions)):
    if int(boxer_predictions[i])==1:
        box_p+=1
    if int(sentClass_predictions[i])==3:
        senC_p+=1
    if int(boxer_predictions[i]) == 1 and int(sentClass_predictions[i]) == 3:
        print(sentences[i-1])
        print('ACTION:',sentences[i])
        print('---------')
        overlap+=1
print('number of actions boxer identified:', box_p)
print('number of actions Sent Class identified:', senC_p)
print('number of equal predictions for actions:',overlap)



