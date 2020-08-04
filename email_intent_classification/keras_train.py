# Authored by kmayank

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM, Convolution1D, Flatten, Dropout, MaxPool1D, Convolution2D, GRU
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
from keras.callbacks import TensorBoard
from EnronDataUtil.ProcessData import getEnronDataForKeras
from keras import optimizers
from keras import callbacks
from sklearn.metrics import f1_score
import pickle

X_train, y_train, X_test, y_test, vocab, word2idx = getEnronDataForKeras()
import csv
w = csv.writer(open("vocab.csv","w"))
for key,val in word2idx.items():
    w.writerow([key,val])
# pickle.dump(word2idx, open("word2idx.pkl", "wb"))
print('vocab length',vocab)
max_length = 100
X_train = sequence.pad_sequences(X_train, maxlen=max_length)
X_test = sequence.pad_sequences(X_test, maxlen=max_length)

embedding_vector_length = 150
model = Sequential()
model.add(Embedding(vocab+1, embedding_vector_length, input_length=max_length))

model.add(Convolution1D(128, 1, border_mode='same'))
model.add(Convolution1D(128, 2, border_mode='same'))
model.add(Convolution1D(128, 3, border_mode='same'))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(200, activation='tanh'))
#-------LSTM
#model.add(LSTM(150))
#model.add(Dropout(0.2))
#-------GRU
# model.add(GRU(150))
# model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model_json = model.to_json()
with open("cnnModel.json", "w") as json_file:
    json_file.write(model_json)
opt = optimizers.Adam(lr=0.00005)
model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
best_weights_filepath = './best_weights.hdf5'
# best = './LSTM150DrpOut2Vector150_best_weights_Train8122Test8253.hdf5'
earlyStopping = callbacks.EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='auto')
saveBestModel = callbacks.ModelCheckpoint(best_weights_filepath, monitor='val_loss', verbose=1, save_best_only=True,
                                          mode='auto')
model.fit(X_train, y_train, nb_epoch=20, validation_split=0.2,
          callbacks=[earlyStopping, saveBestModel], batch_size=30)

model.load_weights(best_weights_filepath)
# model.load_weights(best)
scores = model.evaluate(X_test, y_test, verbose=1)
scoresTrain = model.evaluate(X_train, y_train, verbose=1)
# yPred = model.predict(X_test)
print("Accuracy Train: %.2f%%" % (scoresTrain[1] * 100))
print("Accuracy Test: %.2f%%" % (scores[1] * 100))
