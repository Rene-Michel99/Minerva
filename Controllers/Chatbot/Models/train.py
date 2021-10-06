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

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, self.actual)
net = tflearn.fully_connected(net, self.actual)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=self.epochs, batch_size=10, show_metric=True)

with open("Chatbot/Data/dataV2.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)
    
with open("Chatbot/Data/iniV2.pickle", "wb") as f:
    pickle.dump((self.next_qnt, self.actual, self.epochs), f)

model.save("Chatbot/Data/model_MinervaV2.tflearn")

print('//Neuronios: ',self.actual)