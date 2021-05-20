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

class Chatbot:
    def __init__(self):
        with open("intents.json","r",encoding='utf-8') as file:
            self.data = json.load(file)

        with open("data.pickle", "rb") as f:
            self.words, self.labels, training, output = pickle.load(f)

        tensorflow.reset_default_graph()

        with open("ini.pickle", "rb") as f:
            neuron1, neuron2 ,last_n1,last_n2, epochs= pickle.load(f)

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, last_n2)
        net = tflearn.fully_connected(net, last_n1)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        self.model = tflearn.DNN(net)

        self.model.load("model.tflearn")

    def bag_of_words(self,s,words):
        bag=[0 for _ in range(len(words))]

        s_words=nltk.word_tokenize(s)
        s_words=[stemmer.stem(word.lower()) for word in s_words]
        print(s_words)

        for se in s_words:
            for i, w in enumerate(words):
                if w==se:
                    bag[i]=1
        
        return numpy.array(bag)


    def learn_names(self,learn,inp,responses):
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

    def get_incorrect_predict(self,confidence,inp,pergunta,tag):
        maior=50
        for perg in pergunta:
            x=fuzz.ratio(perg,inp)
            print(x,inp,perg)
            if x>maior:
                maior=x
        if maior<55:
            print('Frase desconhecida',confidence,tag)
            if self.unknow_phrases!=[]:
                for frase in self.unknow_phrases:
                    if fuzz.ratio(frase[0],inp)>90:
                        print('Bot: ',frase[2])
                        return True

            if inp.lower().find('você')!=-1 or inp.lower().find('tu')!=-1 and inp.lower().find('sab')!=-1:
                tag='tag'+str(len(self.labels)+1+len(self.unknow_phrases))
                print('Bot: Não, me conta mais')
                resp=input('Você: ')
            else:
                print('Bot: Não entendi, poderia me explicar o que isso se trata?')
                tag='tag'+str(len(self.labels)+1+len(self.unknow_phrases))
                print('Bot: Como eu poderia responder a isso?')
                resp=input('Você: ')
                print('Bot: Entendi')
            self.unknow_phrases.append([inp,tag,resp])
            return True
        else:
            return False

    def get_accuracy(self):
        with open('teste_extern.json','r',encoding='utf-8') as f:
            teste=json.load(f)
        total=len(teste)
        erros=[]
        cont=0
        for item in teste:
            results=self.model.predict([self.bag_of_words(item['frase'],self.words)])
            results_index=numpy.argmax(results)
            tag=self.labels[results_index]    
            if tag==item['tag']:
                cont+=1
            else:
                erros.append((tag,item['tag']))
        print('Precisão de: ',cont/total)
        print(erros)
        '''
        for tg in self.data['intents']:
            for item in teste:
                if tg['tag']==item['tag']:
                    tg['patterns'].append(item['frase'])

        with open("intents.json","w",encoding='utf-8') as file:
            json.dump(self.data,file,indent=3,ensure_ascii=False)'''
        

    def get_response(self,inp):
        if inp.lower() in self.current_msgs:
            print('Bot: Você já falou isso')
            return 0
        results=self.model.predict([self.bag_of_words(inp,self.words)])
        results_index=numpy.argmax(results)

        tag=self.labels[results_index]
        responses=''
        pergunta=[]

        for tg in self.data['intents']:
            if tg['tag']==tag:
                responses=tg['responses']
                pergunta=tg['patterns']

        if results[0][results_index]<0.65:
            check=self.get_incorrect_predict(results[0][results_index],inp,pergunta,tag)
            if check==False:
                print('Bot: ',random.choice(responses),' //',results[0][results_index])
        else:
            print('Bot: ',random.choice(responses),' //',results[0][results_index])
        self.current_msgs.append(inp.lower())
        

    def chat(self):
        print('Iniciado')

        with open("learn.json") as file:
            learn = json.load(file)
        self.unknow_phrases=[]
        self.current_msgs=[]

        while True:
            inp=input('Você: ')
            if inp.lower()=='quit':
                break
            
            self.get_response(inp)

            print('\nFrases novas: ',self.unknow_phrases)
            
        if self.unknow_phrases!=[]: #aumentar a base de dados talvez implique em aumentar a quantidade neurônios e as epochs
            check=[0 for _ in range(len(self.unknow_phrases))]
            index=0

            for tg in self.data['intents']:
                for unknow in self.unknow_phrases:
                    for pattern in tg['patterns']:
                        if fuzz.ratio(pattern,unknow[0])>90:
                            tg.patterns.append(unknow[0])
                            check[index]=1
                            break
                    index+=1
                index=0
            index=0

            for i in check:
                if i==0:
                    unknow=self.unknow_phrases[index]
                    self.data['intents'].append({'tag':unknow[1],"patterns":[unknow[0]],"responses":[unknow[2]]})
                index+=1

            with open("intents.json","w",encoding='utf-8') as file:
                json.dump(self.data,file,indent=3,ensure_ascii=False)
            self.train(lista=self.unknow_phrases)

    def train(self,lista=[]):
        neuron1=0
        neuron2=0
        with open("ini.pickle", "rb") as f:
            neuron1, neuron2 ,last_n1,last_n2, epochs= pickle.load(f)

        with open("intents.json","r",encoding='utf-8') as file:
            data = json.load(file)

        if lista!=[]:
            if neuron1+len(lista)-5>=last_n1:
                last_n1=neuron1+len(lista)
                epochs+=5+len(lista)
            if neuron2+len(lista)-5>=last_n2:
                last_n2=neuron2+len(lista)
                epochs+=5+len(lista)+10
            neuron1+=len(lista)
            neuron2+=len(lista)
            with open("ini.pickle", "wb") as f:
                pickle.dump((neuron1,neuron2,last_n1,last_n2,epochs), f)

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
        net = tflearn.fully_connected(net, last_n1)
        net = tflearn.fully_connected(net, last_n2)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        model = tflearn.DNN(net)

        model.fit(training, output, n_epoch=epochs, batch_size=10, show_metric=True)
        model.save("model.tflearn")
        print('Neuronios: ',neuron1,neuron2,'//Ultimos: ',last_n1,last_n2)

bot=Chatbot()
bot.chat()