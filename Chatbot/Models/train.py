import tensorflow as tf
import numpy as np
import pickle
import json
import nltk
import random
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

with open("Chatbot/Data/intents.json","r",encoding='utf-8') as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for i,intent in enumerate(data["intents"]):
    intent["tag"] = "tag"+str(i)

with open("Chatbot/Data/intents.json","w",encoding='utf-8') as file:
    json.dump(data,file,indent=3,ensure_ascii=False)

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

ponctuations = ["?","'",'"',"!",".",","]

words = [stemmer.stem(w.lower()) for w in words if w not in ponctuations]
words = sorted(list(set(words)))
labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = np.array(training)
output = np.array(output)

def dense_layers():
    x = tf.keras.layers.Dense(neurons,activation='relu')
    x = tf.keras.layers.Densse(neurons,activation='relu')(x)
    return x

def final_model(inputs):
    model = tf.keras.Model(inputs=inputs,outputs=response)

