# -*- coding: utf-8 -*-

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle

with open("intents.json","r",encoding='utf-8') as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])


words = [stemmer.stem(w.lower()) for w in words if w != "?"]
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


training = numpy.array(training)
output = numpy.array(output)

with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 155)
net = tflearn.fully_connected(net, 155)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=1311, batch_size=10, show_metric=True)
model.save("model.tflearn")


def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]

    s_words=nltk.word_tokenize(s)
    s_words=[stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w==se:
                bag[i]=1
    
    return numpy.array(bag)

def chat():
    print('Iniciado')

    with open("learn.json") as file:
        learn = json.load(file)
    
    while True:
        inp=input('Você: ')
        if inp.lower()=='quit':
            break
        results=model.predict([bag_of_words(inp,words)])
        results_index=numpy.argmax(results)
        tag=labels[results_index]
        responses=''
        for tg in data['intents']:
            if tg['tag']==tag:
                responses=tg['responses']
        
        if tag=="say_name":
            names_knowed=learn["intents"][0]
            check=''
            for name in names_knowed["patterns"]:
                if inp.find(name)!=-1:
                    check=name
            if check!='':
                print('Bot: ',random.choice(names_knowed["responses"]))
            else:
                name=inp[::-1]
                name=name[:name.find(' ')]
                name=name[::-1]
                print('Bot: ',random.choice(responses),name)
        else:
            print('Bot: ',random.choice(responses))

chat()
