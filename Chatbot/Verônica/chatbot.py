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
from fuzzywuzzy import fuzz


with open("intents.json","r",encoding='utf-8') as file:
    data = json.load(file)

with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 150)
net = tflearn.fully_connected(net, 150)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


model.load("model.tflearn")

def bag_of_words(s,words):
    bag=[0 for _ in range(len(words))]

    s_words=nltk.word_tokenize(s)
    s_words=[stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w==se:
                bag[i]=1
    
    return numpy.array(bag)


def learn_names(learn,inp,responses):
    names_knowed=learn
    check=''
    index=0
    name_index=0
    for name in names_knowed["patterns"]:
        if inp.lower().find(name.lower())!=-1:
            check=name
            name_index=index
            index+=1
        if check!='':
            print('Bot: ',names_knowed["responses"][name_index])
        else:
            name=inp[::-1]
            name=name[:name.find(' ')]
            name=name[::-1]
            learn["intents"][0]["patterns"].append(name.title())
            learn["intents"][0]["responses"].append('Ola '+name.title())
            print('Bot: ',random.choice(responses),name)

    with open('learn.json', 'w') as json_file:
        json.dump(learn, json_file)



def chat():
    print('Iniciado')

    with open("learn.json") as file:
        learn = json.load(file)
    unknow_phrases=[]

    while True:
        inp=input('Você: ')
        if inp.lower()=='quit':
            break
        results=model.predict([bag_of_words(inp,words)])
        results_index=numpy.argmax(results)
        
        tag=labels[results_index]
        responses=''
        pergunta=[]
        for tg in data['intents']:
            if tg['tag']==tag:
                responses=tg['responses']
                pergunta=tg['patterns']
        
        if tag=="say_name":
            learn_names(learn["intents"][0],inp,responses)
        else:
            maior=50
            if results[0][results_index]<0.65:
                for perg in pergunta:
                    x=fuzz.token_sort_ratio(inp,perg)
                    print(x,inp,perg)
                    if x>maior:
                        maior=x
                if maior<51:
                    print('termo desconhecido //',results[0][results_index],tag)
                    if inp.lower().find('você')!=-1 or inp.lower().find('tu')!=-1 and inp.lower().find('sab')!=-1:
                        print('Bot: Não, me conta mais')
                        resp=input('Você: ')
                        tag=inp[inp.find('sab')+4]
                    else:
                        print('Bot: Não entendi, poderia me explicar o que isso se trata?')
                        tag=input('Você: ')
                        print('Bot: Como eu poderia responder a isso?')
                        resp=input('Você: ')
                    unknow_phrases.append((inp,tag,resp))
                else:
                    print('Bot: ',random.choice(responses),' //',results[0][results_index],maior)
            else:
                r=results[0]
                r=r[results_index]
                print('Bot: ',random.choice(responses),r)

        print('\nNot learned: ',unknow_phrases)
    
    if unknow_phrases!=[]: #aumentar a base de dados talvez implique em aumentar a quantidade neurônios e as epochs
        check=[0 for _ in range(len(unknow_phrases))]
        index=0

        for tg in data['intents']:
            for unknow in unknow_phrases:
                if tg['tag']==unknow[1]:
                    tg['patterns'].append(unknow[0])
                    check[index]=1
                index+=1
            index=0
        index=0

        for i in check:
            if i==0:
                unknow=unknow_phrases[index]
                data['intents'].append({'tag':unknow[1],"patterns":[unknow[0]],"responses":[unknow[2]]})
            index+=1

        with open("not_learned.json","w",encoding='utf-8') as file:
            json.dump(data,file,indent=3,ensure_ascii=False)

chat()