# -*- coding: utf-8 -*-
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
from fuzzywuzzy import fuzz

class DNN_Model:
    def __init__(self):
        self.current_tag = ""
        
        with open("Chatbot/Data/intents.json","r",encoding='utf-8') as file:
            self.data = json.load(file)

        with open("Chatbot/Data/dataV2.pickle", "rb") as f:
            self.words, self.labels, training, output = pickle.load(f)
        
        tensorflow.reset_default_graph()

        with open("Chatbot/Data/iniV2.pickle", "rb") as f:
            self.next_qnt , self.actual, self.epochs = pickle.load(f)

        net = tflearn.input_data(shape=[None, len(training[0])])
        net = tflearn.fully_connected(net, self.actual)
        net = tflearn.fully_connected(net, self.actual)
        net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
        net = tflearn.regression(net)

        self.model = tflearn.DNN(net)

        self.model.load("Chatbot/Models/model_MinervaV2.tflearn")
        
    def modify_training_values(self,actual,epochs):
        with open("Chatbot/Data/iniV2.pickle", "wb") as f:
            pickle.dump((self.next_qnt, actual, epochs), f)
        
    def get_current_pergs(self):
        return self.current_tag["patterns"]
        
    def bag_of_words(self,s):
        bag = [0 for _ in range(len(self.words))]
        
        ponctuations = ["?","'",'"',"!",".",","]

        s_words = nltk.word_tokenize(s)
        s_words = [stemmer.stem(word.lower()) for word in s_words if word not in ponctuations]

        for se in s_words:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1
        
        return np.array(bag)
    
    def get_prediction(self,inp):
        results = self.model.predict([self.bag_of_words(inp)])
        results_index = np.argmax(results)

        tag = self.labels[results_index]
        responses = ''

        for tg in self.data['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
                self.current_tag = tg
        
        response = random.choice(responses)
        confidence = results[0][results_index]
        
        return response,confidence
    
    def train(self,lista=[]):
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


class Memory:
    def __init__(self):
        self.special_tags = {"<joke>":self.get_joke}
        with open("Chatbot/Music_info/Rock/data.json","r",encoding='utf-8') as f:
            self.base_Mrock = json.loads(f.read())

        _arq = open("Chatbot/Extra_info/piadas.txt","r",encoding='utf-8')
        self.piadas = _arq.read().split("\n")
        _arq.close()
        
    def generate_response(self,resp):
        output = ""
        resp = resp.split()
        
        if len(resp) == 1:
            output = self.special_tags[resp[0]]()
        else:
            tag = ""
            for item in resp:
                if item.find("<")!=-1 and item.find(">")!=-1:
                    tag = item
                    break
            output = self.special_tags[tag]()
        return output
        
    def get_joke(self):
        from random import choice
        return choice(self.piadas)

    
class Chatbot:
    def __init__(self):
        self.dnn = DNN_Model()
        self.unknow_phrases = []
        self.current_questions = []
        self.memory = Memory()

    def get_correct_predict(self,confidence,inp,perguntas):
        maior = 50
        for perg in perguntas:
            x = fuzz.ratio(perg,inp)
            print("Proximity: ",x,inp,perg)
            if x > maior:
                maior = x
                
        if maior < 55:
            print('Frase desconhecida',confidence)
            if self.unknow_phrases!=[]:
                for frase in self.unknow_phrases:
                    if fuzz.ratio(frase[0],inp)>90:
                        return frase[2]

            tag = 'tag'+str(len(self.dnn.labels)+1+len(self.unknow_phrases))
            print('Minerva: Não entendi, como eu poderia responder a isso?')
            resp = input('Você: ')
            out = 'Agora entendi, muito obrigada'
            self.unknow_phrases.append([inp,tag,resp])
            return out
        else:
            return 0
        
    def get_response(self,inp):
        response,confidence = self.dnn.get_prediction(inp)
        
        if confidence < 0.8:
            perguntas = self.dnn.get_current_pergs()
            Sresponse = self.get_correct_predict(confidence,inp,perguntas)
            if Sresponse!=0:
                response = Sresponse

        
        if response.find("<")!=-1 and response.find(">")!=-1 and response in self.memory.special_tags:
            response = self.memory.generate_response(response)
        
        return response

    def chat(self,inp):
        response = self.get_response(inp)
        print('\nFrases novas: ',self.unknow_phrases)
        return response

    def have_to_learn(self):
        if self.unknow_phrases!=[]: #aumentar a base de dados talvez implique em aumentar a quantidade neurônios e as epochs
            check = [0 for _ in range(len(self.unknow_phrases))]
            index = 0
            
            data = self.dnn.data
            
            for tg in data['intents']:
                for unknow in self.unknow_phrases:
                    for pattern in tg['patterns']:
                        if fuzz.ratio(pattern,unknow[0]) > 90:
                            tg["patterns"].append(unknow[0])
                            check[index] = 1
                            break
                    index += 1
                index = 0
            index = 0

            for i in check:
                if i == 0:
                    unknow = self.unknow_phrases[index]
                    data['intents'].append({'tag':unknow[1],"patterns":[unknow[0]],"responses":[unknow[2]]})
                index+=1

            with open("Chatbot/Data/intents.json","w",encoding='utf-8') as file:
                json.dump(data,file,indent=3,ensure_ascii=False)
                
            self.dnn.train(lista=self.unknow_phrases)

#pipe = Chatbot()
#pipe.dnn.train()
