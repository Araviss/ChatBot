import random
import json
import pickle
import numpy as np

import nltk
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.optimizer_v2.gradient_descent import SGD

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
# Lemmatizer uses stem of a word instead of conjugate (performance purposes)
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers i
# mport Dense, Activation, Dropout
# from tensorflow.keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()

# Reading json file, pass to load function, get json object dictionary
intents = json.loads(open('intents.json').read())

words = []
classes = []
documents = []

# Characters that you won't pay attention to
ignore_letters = ['?', '!', '.', ',']

# Splits each pattern entry into individual words
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

#lemmatizes word  inf word list if it is not ignored
words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_letters]
#Set Eliminates duplicate words
words = sorted(set(words))

classes = sorted(set(classes))
#Save the words in file
pickle.dump(words,open('words.pkl','wb'))
#Save classes in file
pickle.dump(classes,open('classes.pkl','wb'))

#CREATING THE TRAINING DATA
#Set individual word values to 0 or 1 depending on whether it occurs
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:#checks to see if word is in pattern
        bag.append(1) if word in word_patterns else bag.append(0)

        output_row = list(output_empty)
        #want to know  class at index 1, want to know index,
        # add class to oupt_row to 1
        output_row[classes.index(document[1])] = 1
        training.append([bag, output_row])

#shuffle the data
random.shuffle(training)
#turn into numpy array
training = np.array(training)

#split into x and y values, Features & Labels
train_x =list(training[:,0])
train_y = list(training[:,1])

#Start building Neural Network Model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5',hist)
print('done')