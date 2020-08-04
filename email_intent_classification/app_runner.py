# Authored by kmayank

from nltk import sent_tokenize, word_tokenize
import pickle
from keras.models import model_from_json
from keras.preprocessing import sequence
import numpy as np

word2idx = pickle.load(open("../saved-models/word2idx.pkl", "rb"))


def preprocess(emailSentences):
    emailSentencesAsArray = []
    splitSentences = False
    for emailSentence in emailSentences:
        tokens = word_tokenize(emailSentence)
        tokenCounter = 0
        if len(tokens) > 100:
            while tokenCounter < len(tokens):
                interTokens = tokens[tokenCounter:tokenCounter + 99]
                sentenceBefore = []
                for t in interTokens:
                    if t not in word2idx:
                        sentenceBefore.append(1)
                    else:
                        sentenceBefore.append(word2idx[t])
                emailSentencesAsArray.append(sentenceBefore)
                tokenCounter += 100
            splitSentences = True
        else:
            sentence = []
            for t in tokens:
                if t not in word2idx:
                    sentence.append(1)
                else:
                    sentence.append(word2idx[t])
            emailSentencesAsArray.append(sentence)
    emailSentencesAsArray = sequence.pad_sequences(emailSentencesAsArray, maxlen=100)
    return emailSentencesAsArray, splitSentences


def getPredictions(modelType, sentences):
    if modelType == "rfc":
        bigram_vectorizer = pickle.load(open("../saved-models/bigramVectorizer.pkl", "rb"))
        preProcessedSentences = bigram_vectorizer.transform(sentences)
        model = pickle.load(open("../saved-models/rfcClassifier.pkl", "rb"))
        predictions = model.predict(preProcessedSentences)
        return predictions, np.ones(predictions.shape), False
    elif modelType == "lstm":
        lstmJson = open("../saved-models/lstmModel.json")
        lstmConfig = lstmJson.read()
        lstmJson.close()
        lstmModel = model_from_json(lstmConfig)
        lstmModel.load_weights("../saved-models/LSTM150Lr0025DrpOut2Vector150_best_weights_Train9080Test8061.hdf5")
        lstmModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        lstmPreprocessedData, splitSentences = preprocess(sentences)
        lstmPredictions = lstmModel.predict(lstmPreprocessedData)
        roundedLstmPredictions = np.round(lstmPredictions)
        return roundedLstmPredictions, lstmPredictions, splitSentences
    elif modelType == "cnn":
        cnnJson = open("../saved-models/cnnModel.json")
        cnnConfig = cnnJson.read()
        cnnJson.close()
        cnnModel = model_from_json(cnnConfig)
        cnnModel.load_weights(
            "../saved-models/CNN128112821283DrpOut2Dense200TanhLr025Vector150_best_weights_Train9107Test8061.hdf5")
        cnnModel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        cnnPreprocessedData, splitSentences = preprocess(sentences)
        cnnPredictions = cnnModel.predict(cnnPreprocessedData)
        roundedCnnPredictions = np.round(cnnPredictions)
        return roundedCnnPredictions, cnnPredictions, splitSentences
    else:
        print("Unsupported model type")


# text = "Hi Mayank, I think we need to meet soon. Friday was pretty hectic, I will relax at home over the weekend. I will see you first thing Monday."
# text = "Jane, We need to look into why tread dump being generated during integration tests. " \
#        "John, Sleep is happening in ruby code. There are two reasons why I do this. " \
#        "To verify reset log level functionality – reset duration is in terms of minutes, so to verify the " \
#        "log configuration after reset is complete, i do a sleep of 62seconds. Right now there are two scenarios" \
#        " where I test reset behaviour. Can verify if it is possible to manage with only one of them. " \
#        "To cover negative scenarios, i had to use improper logback.xml configuration. " \
#        "I’m doing that replacement and waiting 40seconds for configuration refresh to happen. " \
#        "I have set refresh duration as 30 seconds in application.properties. " \
#        "I can try reducing it further, and hence the sleep time."
# text = "Hi Bhavesh, Thanks for the response. Would it be possible to clarify the items in question " \
#        "with Google? I’ve attached the latest matrix for reference. " \
#        "Additionally, Adam and I consulted with the PMs and decided to remove the Samsung column" \
#        " as it will be nearly impossible to keep this accurate and up to date. Does anyone have any " \
#        "objections to removing this column? Thanks,Kelly"
voting = False
emailFileNames = []
emailPredicitions = []
for i in range(1, 2):
    emailFileNames.append("email" + str(i) + ".txt")
# emailFileNames.append("email1.txt")
for emailFileName in emailFileNames:
    filePath = "../test-emails/"
    completePath = filePath + emailFileName
    text = open(completePath, encoding="utf8").read()
    sentences = sent_tokenize(text)
    if voting:
        predictions, confidence, splitSentences = getPredictions("rfc", sentences)
        predictions, confidence, splitSentences = getPredictions("lstm", sentences)
        predictions, confidence, splitSentences = getPredictions("cnn", sentences)
    else:
        predictions, confidence, splitSentences = getPredictions("lstm", sentences)
    actionable = []
    nonactionable = []
    splitSentence = []
    if splitSentences:
        for sentence in sentences:
            tokens = word_tokenize(sentence)
            tokenCounter = 0
            if len(tokens) > 100:
                while tokenCounter < len(tokens):
                    interTokens = tokens[tokenCounter:tokenCounter + 99]
                    splitSentence.append(' '.join(interTokens))
                    tokenCounter += 100
            else:
                splitSentence.append(' '.join(tokens))
        sentences = splitSentence
    for idx in range(len(predictions)):
        if predictions[idx] == 1:
            actionable.append((confidence[idx][0], sentences[idx]))
            # print("Actionable Items:", (confidence[idx][0], sentences[idx]))
        else:
            nonactionable.append((confidence[idx][0], sentences[idx]))
            # print("Non-actionable Items:", (1 - confidence[idx][0], sentences[idx]))

    print("Actionable Items:", actionable)
    print("Non-actionable Items:", nonactionable)
    print(" ")
    emailPredicitions.append((completePath, actionable))

print(emailPredicitions)
