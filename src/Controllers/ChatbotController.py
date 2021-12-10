# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import random
import json
import pickle
import spacy
from fuzzywuzzy import fuzz

class Data:
    def __init__(self):
        self.current_tag = ""
        try:
            self.nlp = spacy.load('pt_core_news_sm')
        except:
            from os import popen
            status = popen("python -m spacy download pt_core_news_sm").read()
            self.nlp = spacy.load('pt_core_news_sm')

        with open("Chatbot/Data/intents.json","r",encoding='utf-8') as file:
            self.dataset = json.load(file)
        
        with open("Chatbot/Data/dataV2.pickle", "rb") as f:
            self.words, self.labels, _, _ = pickle.load(f)


class DNN_Model:
    def __init__(self):
        self.data = Data()
        self.model = tf.keras.models.load_model("./Chatbot/Models/model.h6")
        
    def modify_training_values(self,actual,epochs):
        self.data.modify_training_values(actual,epochs)
        
    def get_current_pergs(self):
        return self.data.current_tag["patterns"]
        
    def bag_of_words(self,s):
        bag = [0 for _ in range(len(self.data.words))]
        ponctuations = ["?","'",'"',"!",".",",",":",";"]
        
        doc = self.data.nlp(s.lower())
        s_words = []
        for token in doc:
            if not token.is_stop and token.lemma_ not in ponctuations:
                s_words.append(token.lemma_)

        for se in s_words:
            for i, w in enumerate(self.data.words):
                if w == se:
                    bag[i] = 1
        
        return np.array(bag)
        
    
    def get_prediction(self,inp):
        bag = self.bag_of_words(inp)
        bag = bag.reshape((1,len(self.data.words)))

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

    
class ChatbotController:
    def __init__(self):
        self.dnn = DNN_Model()
        self.unknow_phrases = []
        self.current_questions = []
        self.memory = Memory()
        self.min_confidence = 0.6
        self.wait_new_phrase = 0

    def get_correct_predict(self,confidence,inp,perguntas):
        maior = 50
        for perg in perguntas:
            x = fuzz.ratio(perg,inp)
            print("Proximity: ",x,inp,perg)
            if x > maior:
                maior = x
                
        if maior < 40:
            print('Frase desconhecida',confidence)
            if self.unknow_phrases!=[]:
                for frase in self.unknow_phrases:
                    if fuzz.ratio(frase[0],inp)>90:
                        return frase[2]

            tag = 'tag'+str(len(self.dnn.data.labels)+1+len(self.unknow_phrases))
            self.unknow_phrases.append([inp,tag,"NONE"])
            self.wait_new_phrase = len(self.unknow_phrases)-1
            return 'Não entendi, como eu poderia responder a isso?'
        else:
            return 0
        
    def get_response(self,inp):
        response,confidence = self.dnn.get_prediction(inp)
        
        if confidence < self.min_confidence:
            perguntas = self.dnn.get_current_pergs()
            Sresponse = self.get_correct_predict(confidence,inp,perguntas)
            if Sresponse!=0:
                response = Sresponse

        
        if response.find("<")!=-1 and response.find(">")!=-1 and response in self.memory.special_tags:
            response = self.memory.generate_response(response)
        
        return response

    def chat(self,inp):
        if self.wait_new_phrase and inp.lower() != "cancelar":
            tag = self.wait_new_phrase
            self.unknow_phrases[tag][2] = inp
            self.wait_new_phrase = 0
            return 'Agora entendi, muito obrigada'
        elif inp == "cancelar":
            self.unknow_phrases.pop()
            return "Entendido"
        else:
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
