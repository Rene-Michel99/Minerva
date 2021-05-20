# -*- coding: utf-8 -*-
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
import random
import json
import pickle
from fuzzywuzzy import fuzz

class Data:
    def __init__(self):
        self.current_tag = ""

        with open("Chatbot/Data/intents.json","r",encoding='utf-8') as file:
            self.dataset = json.load(file)
        
        with open("Chatbot/Data/dataV2.pickle", "rb") as f:
            self.words, self.labels, training, output = pickle.load(f)

        with open("Chatbot/Data/iniV2.pickle", "rb") as f:
            self.next_qnt , self.NEURONS, self.EPOCHS = pickle.load(f)
        
        self.stopwords = nltk.corpus.stopwords.words('portuguese')
    
    def modify_training_values(self,actual,epochs):
        with open("Chatbot/Data/iniV2.pickle", "wb") as f:
            pickle.dump((self.next_qnt, actual, epochs), f)


class DNN_Model:
    def __init__(self):
        self.data = Data()

        self.model = tf.keras.models.load_model("./Chatbot/Models/model.h5")
        
    def modify_training_values(self,actual,epochs):
        self.data.modify_training_values(actual,epochs)
        
    def get_current_pergs(self):
        return self.data.current_tag["patterns"]
        
    def bag_of_words(self,s):
        bag = [0 for _ in range(len(self.data.words))]
        
        ponctuations = ["?","'",'"',"!",".",","]

        s_words = nltk.word_tokenize(s)
        s_words = [word for word in s_words if word.lower() not in self.data.stopwords]
        s_words = [stemmer.stem(word.lower()) for word in s_words if word not in ponctuations]

        for se in s_words:
            for i, w in enumerate(self.data.words):
                if w == se:
                    bag[i] = 1
        
        return np.array(bag)
    
    def get_prediction(self,inp):
        bag = self.bag_of_words(inp)
        bag = bag.reshape((1,493))

        results = self.model.predict(bag)
        results_index = np.argmax(results)

        tag = self.data.labels[results_index]
        responses = ''

        for tg in self.data.dataset['intents']:
            if tg['tag'] == tag:
                responses = tg['responses']
                self.data.current_tag = tg
        
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
        
        words  = [w for w in words if w.lower() not in self.data.stopwords]
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
        SHAPE = len(training[0])
        N_CLASSES = len(output[0])

        model = self.define_and_compile_model(SHAPE,N_CLASSES,self.data.NEURONS)
        model.fit(training,output,epochs=self.data.EPOCHS)

        with open("Chatbot/Data/dataV2.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)
            
        with open("Chatbot/Data/iniV2.pickle", "wb") as f:
            pickle.dump((self.data.next_qnt, self.data.NEURONS, self.data.EPOCHS), f)

        model.save("Chatbot/Data/model.h5")
        
        print('//Neuronios: ',self.data.NEURONS)
    
    def dense_layers(self,inputs,NEURONS):
        x = tf.keras.layers.Dense(NEURONS,activation='relu')(inputs)
        x = tf.keras.layers.Dense(NEURONS,activation='relu')(x)
        x = tf.keras.layers.Dense(NEURONS,activation='relu')(x)
        return x

    def classfier_layer(self,x,N_CLASSES):
        x = tf.keras.layers.Dense(N_CLASSES,activation='softmax',name='classification')(x)
        return x

    def final_model(self,inputs,N_CLASSES,NEURONS):
        dense = self.dense_layers(inputs,NEURONS)
        
        classfier = self.classfier_layer(dense,N_CLASSES)
        
        model = tf.keras.Model(inputs=inputs,outputs=classfier)
        
        return model
        
    def define_and_compile_model(self,SHAPE,N_CLASSES,NEURONS):
        inputs = tf.keras.layers.Input(shape=(SHAPE,))
        
        # create the model
        model = self.final_model(inputs,N_CLASSES,NEURONS)
        
        # compile your model
        model.compile(optimizer='adam',loss='binary_crossentropy',metrics = {'classification' : 'accuracy'})

        return model


class Memory:
    def __init__(self):
        self.special_tags = {"<joke>":self.get_joke}
        with open("Chatbot/Music_info/Rock/data.json","r",encoding='utf-8') as f:
            self.base_Mrock = json.loads(f.read())

        _arq = open("Chatbot/Extra_info/Piadas.txt","r",encoding='utf-8')
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

            tag = 'tag'+str(len(self.dnn.data.labels)+1+len(self.unknow_phrases))
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
