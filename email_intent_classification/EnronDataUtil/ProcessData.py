# Authored by kmayank

import numpy as np
import pandas as pd
from tensorflow.contrib import learn
from sklearn.feature_extraction.text import CountVectorizer
from nltk import pos_tag, word_tokenize
from keras.preprocessing import sequence as sq
import string
import pickle


def getEnronTrainingData():
    data = pd.read_csv('../resources/training-data.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-data.txt', sep='^', header=None)
    testData = test.as_matrix()

    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    max_length = max([len(x.split(" ")) for x in xTrain])
    vocab_processor = learn.preprocessing.VocabularyProcessor(max_length)
    xPreprocess = np.array(list(vocab_processor.fit_transform(xTrain)))
    xPreprocessTest = np.array(list(vocab_processor.transform(xTest)))
    vocab_processor_label = learn.preprocessing.VocabularyProcessor(1)
    yPreprocess = np.array(list(vocab_processor_label.fit_transform(yTrain)))
    N = len(yPreprocess)
    for i in range(N):
        if yPreprocess[i] == 1:
            yPreprocess[i] = 0
        if yPreprocess[i] == 2:
            yPreprocess[i] = 1

    yPreprocess = yPreprocess.astype(np.int32)
    ind = np.zeros((N, 2))
    for i in range(N):
        ind[i, yPreprocess[i]] = 1
    yPreprocess = ind

    yPreprocessTest = np.array(list(vocab_processor_label.fit_transform(yTest)))
    NTest = len(yPreprocessTest)
    for iTest in range(NTest):
        if yPreprocessTest[iTest] == 1:
            yPreprocessTest[iTest] = 0
        if yPreprocessTest[iTest] == 2:
            yPreprocessTest[iTest] = 1

    yPreprocessTest = yPreprocessTest.astype(np.int32)
    indTest = np.zeros((NTest, 2))
    for iTest in range(NTest):
        indTest[iTest, yPreprocessTest[iTest]] = 1
    yPreprocessTest = indTest

    return np.array(xPreprocess), np.array(yPreprocess), np.array(xPreprocessTest), np.array(yPreprocessTest), max_length


def getTags(line):
    tuples = pos_tag(word_tokenize(line))
    return [y for x, y in tuples]


def pad(l, size, padding):
    return l + [padding] * abs((len(l)-size))

def getEnronTrainingDataPOS():
    data = pd.read_csv('../resources/training-data.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-data.txt', sep='^', header=None)
    testData = test.as_matrix()

    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    max_length = 0

    xPos = []
    word2idx = {'UNK': 0}
    current_idx = 1
    for line in xTrain:
        tokens = getTags(line)
        if tokens.__len__() > max_length:
            max_length = tokens.__len__()
        for token in tokens:
            if token not in word2idx:
                word2idx[token] = current_idx
                current_idx += 1
        sequence = np.array([word2idx[w] for w in tokens])
        xPos.append(sequence)

    xPreprocess = np.array(xPos)

    xPosTest = []
    for lineTest in xTest:
        tokensTest = getTags(lineTest)
        for tokenTest in tokensTest:
            if tokenTest not in word2idx:
                word2idx[tokenTest] = 0
        sequenceTest = np.array([word2idx[w] for w in tokensTest])
        xPosTest.append(sequenceTest)

    xPreprocessTest = np.array(xPosTest)

    vocab_processor_label = learn.preprocessing.VocabularyProcessor(1)
    yPreprocess = np.array(list(vocab_processor_label.fit_transform(yTrain)))
    N = len(yPreprocess)
    for i in range(N):
        if yPreprocess[i] == 1:
            yPreprocess[i] = 0
        if yPreprocess[i] == 2:
            yPreprocess[i] = 1

    yPreprocess = yPreprocess.astype(np.int32)
    ind = np.zeros((N, 2))
    for i in range(N):
        ind[i, yPreprocess[i]] = 1
    yPreprocess = ind

    yPreprocessTest = np.array(list(vocab_processor_label.fit_transform(yTest)))
    NTest = len(yPreprocessTest)
    for iTest in range(NTest):
        if yPreprocessTest[iTest] == 1:
            yPreprocessTest[iTest] = 0
        if yPreprocessTest[iTest] == 2:
            yPreprocessTest[iTest] = 1

    yPreprocessTest = yPreprocessTest.astype(np.int32)
    indTest = np.zeros((NTest, 2))
    for iTest in range(NTest):
        indTest[iTest, yPreprocessTest[iTest]] = 1
    yPreprocessTest = indTest
    xPreprocess = sq.pad_sequences(xPreprocess, maxlen=max_length, padding='post')
    xPreprocessTest = sq.pad_sequences(xPreprocessTest, maxlen=max_length, padding='post')
    return xPreprocess, np.array(yPreprocess), xPreprocessTest, np.array(yPreprocessTest), max_length

def remove_punctuation(s):
    return s.translate(string.punctuation)


def getEnronDataForKeras():
    data = pd.read_csv('./resources/training-cleaned.txt', sep='^', header=None)
    #trainData = data.as_matrix()
    trainData = data.to_numpy()
    test = pd.read_csv('./resources/testing-cleaned.txt', sep='^', header=None)
    #testData = test.as_matrix()
    testData = test.to_numpy()
    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    max_len = 0
    word2idx ={'UNK':1}
    currentIdx = 2
    xPreprocess = []
    for x in xTrain:
        tokens = word_tokenize(x)
        if len(tokens) > max_len:
            max_len = len(tokens)
        for t in tokens:
            if t not in word2idx:
                word2idx[t] = currentIdx
                currentIdx += 1
        sentences = [word2idx[w] for w in tokens]
        xPreprocess.append(sentences)

    xPreprocessTest = []
    for xTest in xTest:
        tokensTest = word_tokenize(xTest)
        sentence = []
        for tTest in tokensTest:
            if tTest not in word2idx:
                sentence.append(1)
            else:
                sentence.append(word2idx[tTest])
        xPreprocessTest.append(sentence)

    # vocab_processor_label = learn.preprocessing.VocabularyProcessor(1)
    # yPreprocess = list(vocab_processor_label.fit_transform(np.transpose(yTrain)))
    # yLabel = []
    # for data in yPreprocess:
    #     for label in data:
    #         yLabel.append(label)
    #
    # yPreprocessTest = list(vocab_processor_label.fit_transform(np.transpose(yTest)))
    # yLabelTest = []
    # for dataTest in yPreprocessTest:
    #     for labelTest in dataTest:
    #         yLabelTest.append(labelTest)
    #
    # xPreprocess = np.array(xPreprocess)
    # xPreprocessTest = np.array(xPreprocessTest)
    # yLabel = np.array(yLabel)
    # yLabelTest = np.array(yLabelTest)
    return xPreprocess, yTrain, xPreprocessTest, yTest, len(word2idx), word2idx


def getEnronTrainingDataForRFC():
    data = pd.read_csv('../resources/training-data.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-data.txt', sep='^', header=None)
    testData = test.as_matrix()
    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
    xPreprocess = bigram_vectorizer.fit_transform(xTrain).toarray()
    xPreprocessTest = bigram_vectorizer.transform(xTest).toarray()
    vocab_processor_label = learn.preprocessing.VocabularyProcessor(1)
    yPreprocess = list(vocab_processor_label.fit_transform(np.transpose(yTrain)))
    yLabel = []
    for data in yPreprocess:
        for label in data:
            yLabel.append(label-1)

    yPreprocessTest = list(vocab_processor_label.fit_transform(np.transpose(yTest)))
    yLabelTest = []
    for dataTest in yPreprocessTest:
        for labelTest in dataTest:
            yLabelTest.append(labelTest-1)

    return xPreprocess, yLabel, xPreprocessTest, yLabelTest, bigram_vectorizer


def getCleanedEnronTrainingDataForRFC():
    data = pd.read_csv('../resources/training-cleaned.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-cleaned.txt', sep='^', header=None)
    testData = test.as_matrix()
    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
    xPreprocess = bigram_vectorizer.fit_transform(xTrain).toarray()
    xPreprocessTest = bigram_vectorizer.transform(xTest).toarray()
    yLabel = []
    for data in yTrain:
            yLabel.append(data)

    yLabelTest = []
    for dataTest in yTest:
            yLabelTest.append(dataTest)

    return xPreprocess, yLabel, xPreprocessTest, yLabelTest, bigram_vectorizer

def getEnronPosTaggedDataForRFC():
    data = pd.read_csv('../resources/training-data.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-data.txt', sep='^', header=None)
    testData = test.as_matrix()

    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    xPosTrain = []
    for x in xTrain:
        xSent = ''
        posTags = pos_tag(word_tokenize(x))
        for chunks in posTags:
            xSent += chunks[0] + ' ' + chunks[1] + ' '
        xPosTrain.append(xSent)

    xPreprocessPos = np.array(xPosTrain)

    xPosTest = []
    for xPosTestEle in xTest:
        xSentEle = ''
        posTags = pos_tag(word_tokenize(xPosTestEle))
        for chunksEle in posTags:
            xSentEle += chunksEle[0] + ' ' + chunksEle[1] + ' '
        xPosTest.append(xSentEle)

    xPreprocessPosTest = np.array(xPosTest)

    bigram_vectorizer = CountVectorizer(ngram_range=(1, 2), token_pattern=r'\b\w+\b', min_df=1)
    xPreprocess = bigram_vectorizer.fit_transform(xPreprocessPos).toarray()
    xPreprocessTest = bigram_vectorizer.transform(xPreprocessPosTest).toarray()
    vocab_processor_label = learn.preprocessing.VocabularyProcessor(1)
    yPreprocess = list(vocab_processor_label.fit_transform(np.transpose(yTrain)))
    yLabel = []
    for data in yPreprocess:
        for label in data:
            yLabel.append(label)

    yPreprocessTest = list(vocab_processor_label.fit_transform(np.transpose(yTest)))
    yLabelTest = []
    for dataTest in yPreprocessTest:
        for labelTest in dataTest:
            yLabelTest.append(labelTest)

    return xPreprocess, yLabel, xPreprocessTest, yLabelTest


def getEnronOnlyPosTrainingDataForRFC():
    data = pd.read_csv('../resources/training-data.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-data.txt', sep='^', header=None)
    testData = test.as_matrix()

    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    max_length = 0

    xPos = []
    word2idx = {'UNK': 0}
    current_idx = 1
    for line in xTrain:
        tokens = getTags(line)
        if tokens.__len__() > max_length:
            max_length = tokens.__len__()
        for token in tokens:
            if token not in word2idx:
                word2idx[token] = current_idx
                current_idx += 1
        sequence = np.array([word2idx[w] for w in tokens])
        xPos.append(sequence)

    xPreprocess = np.array(xPos)

    xPosTest = []
    for lineTest in xTest:
        tokensTest = getTags(lineTest)
        for tokenTest in tokensTest:
            if tokenTest not in word2idx:
                word2idx[tokenTest] = 0
        sequenceTest = np.array([word2idx[w] for w in tokensTest])
        xPosTest.append(sequenceTest)

    xPreprocessTest = np.array(xPosTest)

    xPreprocess = sq.pad_sequences(xPreprocess, maxlen=max_length, padding='post')
    xPreprocessTest = sq.pad_sequences(xPreprocessTest, maxlen=max_length, padding='post')

    vocab_processor_label = learn.preprocessing.VocabularyProcessor(1)
    yPreprocess = list(vocab_processor_label.fit_transform(np.transpose(yTrain)))
    yLabel = []
    for data in yPreprocess:
        for label in data:
            yLabel.append(label)

    yPreprocessTest = list(vocab_processor_label.fit_transform(np.transpose(yTest)))
    yLabelTest = []
    for dataTest in yPreprocessTest:
        for labelTest in dataTest:
            yLabelTest.append(labelTest)

    return xPreprocess, yLabel, xPreprocessTest, yLabelTest

def init_weight(Mi, Mo):
    return np.random.randn(Mi, Mo) / np.sqrt(Mi + Mo)


def getEnronCleanedData():
    data = pd.read_csv('../resources/training-cleaned.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-cleaned.txt', sep='^', header=None)
    testData = test.as_matrix()

    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    max_len = 0
    word2idx ={'UNK':1}
    currentIdx = 2
    xPreprocess = []
    for x in xTrain:
        tokens = word_tokenize(x)
        if len(tokens) > max_len:
            max_len = len(tokens)
        for t in tokens:
            if t not in word2idx:
                word2idx[t] = currentIdx
                currentIdx += 1
        sentences = np.array([word2idx[w] for w in tokens])
        xPreprocess.append(sentences)

    xPreprocess = np.array(sq.pad_sequences(xPreprocess, 100, padding='post'))

    xPreprocessTest = []
    for xTest in xTest:
        tokensTest = word_tokenize(xTest)
        sentence = []
        for tTest in tokensTest:
            if tTest not in word2idx:
                sentence.append(1)
            else:
                sentence.append(word2idx[tTest])
        sentencesTest = np.array(sentence)
        xPreprocessTest.append(sentencesTest)

    xPreprocessTest = np.array(sq.pad_sequences(xPreprocessTest, 100, padding='post'))

    NTrain = len(yTrain)
    indTrain = np.zeros((NTrain, 2))
    for iTrain in range(NTrain):
        indTrain[iTrain, yTrain[iTrain]] = 1
    yPreprocessTrain = indTrain

    NTest = len(yTest)
    indTest = np.zeros((NTest, 2))
    for iTest in range(NTest):
        indTest[iTest, yTest[iTest]] = 1
    yPreprocessTest = indTest

    return xPreprocess, yPreprocessTrain, xPreprocessTest, yPreprocessTest, 100

def test():
    data = pd.read_csv('../resources/training-data.txt', sep='^', header=None)
    trainData = data.as_matrix()
    test = pd.read_csv('../resources/testing-data.txt', sep='^', header=None)
    testData = test.as_matrix()

    xTrain = trainData[:, 1]
    yTrain = trainData[:, 0]

    xTest = testData[:, 1]
    yTest = testData[:, 0]

    countTrain = 0
    idx = 0
    for x in xTrain:
        idx += 1
        if(len(word_tokenize(x)) > 100):
            countTrain += 1
            print(idx)
    countTest = 0
    idxTest = 0
    for x in xTest:
        idxTest += 1
        if (len(word_tokenize(x)) > 100):
            countTest += 1
            print(idxTest)
    print(countTrain)
    print(countTest)

if __name__ == '__main__':
    getCleanedEnronTrainingDataForRFC()
