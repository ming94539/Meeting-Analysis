import collections
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
#from tqdm import tqdm
#import BERTSentiment
SID = SentimentIntensityAnalyzer()
def get_sentiment(text, type="nltk"):
    sents = tokenize.sent_tokenize(text)
    scores = collections.defaultdict(float)
    for sent in sents:
        if type == "nltk":
            model_scores = SID.polarity_scores(sent)
        else:
            model_scores = BERTSentiment.predict_sentiment(sent)
        for feel in ['neg', 'neu', 'pos']:
            scores[feel] += model_scores[feel]
    return scores
def get_speaker_sentiments(text, type="nltk"):
    speaker_sentiments = collections.defaultdict(collections.defaultdict)
    speaker_time_sentiments = collections.defaultdict(collections.defaultdict)
    length = 0
    lines = text.split('\n')
    for line in lines:
        if line == '\n':
            continue
        colon_ind = line.find(":")
        if colon_ind != -1:
            speaker = line[:colon_ind].strip()
            text = line[colon_ind+1:].replace('\n', ' ')
        else:
            # keep same speaker
            text = line.replace('\n', ' ')
        length += len(text)
    length_ingested = 0
    n = 1
    curr_sentiments = collections.defaultdict(list)
    print("Processing sentiment")
    for line in lines:
        if line == '\n':
            continue
        colon_ind = line.find(":")
        if colon_ind != -1:
            speaker = line[:colon_ind].strip()
            text = line[colon_ind+1:].replace('\n', ' ')
        else:
            # keep same speaker
            text = line.replace('\n', ' ')
        length_ingested += len(text)
        if length_ingested/length > n * 0.05:
            for speaker in curr_sentiments:
                speaker_time_sentiments[speaker][round(n*0.05, 2)] = sum(curr_sentiments[speaker])/len(curr_sentiments[speaker])
            curr_sentiments = collections.defaultdict(list)
            n += 1
        sentiment = get_sentiment(text, type)
        score = sentiment['pos'] - sentiment['neg']
        curr_sentiments[speaker].append(score)
        if speaker in speaker_sentiments:
            for feel in ['neg', 'neu', 'pos']:
                speaker_sentiments[speaker][feel] += sentiment[feel]
        else:
            for feel in ['neg', 'neu', 'pos']:
                speaker_sentiments[speaker][feel] = sentiment[feel]
    for speaker in curr_sentiments:
        speaker_time_sentiments[speaker][round(n*0.05, 2)] = sum(curr_sentiments[speaker])/len(curr_sentiments[speaker])
    formatted_speaker_sentiments = {}
    for speaker, sentiments in speaker_sentiments.items():
        neg = sentiments['neg']
        neu = sentiments['neu']
        pos = sentiments['pos']
        all = neg + neu + pos
        neg_prop, neu_prop, pos_prop = neg/all, neu/all, pos/all
        formatted_speaker_sentiments[speaker] = {'Positive': round(pos_prop, 2),
                                                 'Negative': round(neg_prop, 2),
                                                 'Neutral': round(neu_prop, 2)}
    formatted_speaker_time_sentiments = {}
    for speaker, times in speaker_time_sentiments.items():
        formatted_speaker_time_sentiments[speaker] = {}
        for time in times:
             formatted_speaker_time_sentiments[speaker][time] = round(speaker_time_sentiments[speaker][time], 2)
    return formatted_speaker_sentiments, formatted_speaker_time_sentiments
