# -*- coding: utf-8 -*-

import datetime

def translate(text):
    day=text[:text.find(':')]
    text=text[text.find(':')+1:]

    day_number=text[:text.find(':')].replace(':','')
    month=text[text.find(':'):].replace(':','')
    days={'Monday':'Segunda','Tuesday':'Terça','Wednesday':'Quarta','Thursday':'Quinta','Friday':'Sexta','Saturday':'Sábado','Sunday':'Domingo'}
    months={'Jan':'Janeiro','Feb':'Fevereiro','Mar':'Março','Apr':'Abril','May':'Maio','Jun':'Junho','Jul':'Julho','Aug':'Agosto','Sep':'Setembro','Oct':'Outubro','Nov':'Novembro','Dec':'Dezembro'}

    t_month=months[month]
    t_day=days[day]
    string='Hoje é '+t_day+' '+day_number+' de '+t_month+' de '+datetime.datetime.now().strftime("%Y")
    return string

def get_day(day):
    days={'Monday':'segunda-feira','Tuesday':'terça-feira','Wednesday':'quarta-feira','Thursday':'quinta-feira','Friday':'sexta-feira','Saturday':'sábado','Sunday':'domingo'}
    return days[day]

def get_the_status(time):
    if int(time)>=5 and int(time)<=12:
        return 'Manhã'
    elif int(time)>=13 and int(time)<=17:
        return 'Tarde'
    else:
        return 'Noite'

def three_more_cheap(lista):
    menor1=[0,0,99999999999]
    menor2=[0,0,99999999999]
    menor3=[0,0,99999999999]
    for item in lista:
        if item[2]<menor1[2]:
            menor1=item
        elif item[2]<menor2[2]:
            menor2=item
        elif item[2]<menor3[2]:
            menor3=item
    
    string='O mais barato é '+menor1[0]+' no site '+menor1[1]+' custando '+str(menor1[2])+' reais'
    return string
    
def structurize_data_hardware(pct_b,disk_u,cpu_d,cpu2):
    if pct_b <= 20 or disk_u.percent > 80 or cpu_d > 75:
        text = 'Tomei a liberdade de analisar um pouco o hardware,'
        if pct_b <= 20:
            text += 'A bateria se encontra em'+str(pct_b)+'% , sujiro que coloque para carregar,'
        if disk_u.percent > 80:
            text += 'Mais de'+str(round(disk_u.percent))+'%'+' da memória principal está em uso, posso deletar algumas coisas caso desejar,'
        if cpu_d > 75:
            text += 'A cpu está sendo bastante usada, o valor atual é de'+str(cpu_d)
        return text
    return None

def solve_math(problem):
    if problem.find('quanto é ')!=-1:
        problem=problem.replace('quanto é ','')
    elif problem.find('resolva')!=-1:
        problem=problem.replace('resolva','')
    elif problem.find('calcule')!=-1:
        problem=problem.replace('calcule','')

    import re
    if problem.find('vezes')!=-1 or problem.find('x')!=-1:
        problem=problem.replace('vezes','*')
        problem=problem.replace('x','*')
    if problem.find('mais')!=-1:
        problem=problem.replace('mais','+')
    if problem.find('dividido')!=-1:
        problem=problem.replace('dividido','/')
    if problem.find('menos')!=-1:
        problem=problem.replace('menos','-')
    if problem.find(' ao quadrado')!=-1:
        problem=problem.replace(' ao quadrado','**2')
    if problem.find(' ao cubo')!=-1:
        problem=problem.replace(' ao quadrado','**3')
    if problem.find('raiz quadrada de ')!=-1:
        pos=problem.find('raiz quadrada de ')+16
        number=problem[pos+1:]
        if number.find(' ')!=-1:
            number=number[:number.find(' ')]
        from math import sqrt
        sq=' '+str(round(sqrt(int(number))))
        to_rp='raiz quadrada de '+number
        problem=problem.replace(to_rp, sq)
        problem=problem.replace('a','')

    return eval(problem)

def play_sound_init():
    import pygame

    sound='Sounds/lbpnotification.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def play_sound_end():
    import pygame

    sound='Sounds/tethys.mp3'
    pygame.mixer.init()
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def get_palavras():
    data=[]
    arq=open('Vocabulario/Non_Asks.txt','r',encoding='utf-8')
    for linha in arq:
        new_line=linha.replace('\n','')
        new_line=new_line.lower()
        data.append(new_line)
    print(data)
    
    import spacy
    copy_data=data
    nlp=spacy.load('pt_core_news_sm')
    lemmas=[]
    structs=[]
    asks=[]
    arq=open('Analise4.txt','w',encoding='utf-8')
    for text in copy_data:
        doc=nlp(text[text.find(':')+2:])
        for token in doc:
            lemmas.append(token.lemma_)
            structs.append(token.pos_+'/'+token.tag_)
        #if '?' in lemmas:
            asks.append(str(lemmas)+'\n'+str(structs)+'\n\n')
        arq.write(str(lemmas)+'\n'+str(structs)+'\n\n')
        lemmas=[]
        structs=[]
    arq.close()
    '''
    arq=open('Perguntas3.txt','w',encoding='utf-8')
    for i in asks:
        arq.write(i+'\n\n')
    arq.close()
    '''
    '''
    lemmas=[]
    structs=[]
    for token in doc:
        lemmas.append(token.lemma_)
        structs.append(token.pos_+'/'+token.tag_)
        #print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha)
    print(lemmas)
    print(structs)'''

def count_sentences():
    arq=open('Analise4.txt','r',encoding='utf-8')
    countADJ=0
    countVERB=0
    countPRON=0
    countCCONJ=0
    countSCONJ=0
    countNOUN=0
    countADP=0
    countADV=0
    countall=0
    for linha in arq:
        countall+=1
        if linha.find('ADJ')!=-1:
            countADJ+=1
        if linha.find('VERB')!=-1:
            countVERB+=1
        if linha.find('PRON')!=-1:
            countPRON+=1
        if linha.find('CCONJ')!=-1:
            countCCONJ+=1
        if linha.find('SCONJ')!=-1:
            countSCONJ+=1
        if linha.find('NOUN')!=-1:
            countNOUN+=1
        if linha.find('ADP')!=-1:
            countADP+=1
        if linha.find('ADV')!=-1:
            countADV+=1
    arq.close()
    print('ADJ: ',countADJ,'/VERB: ',countVERB,'/PRON: ',countPRON,'/CCONJ: ',countCCONJ,'/SCONJ: ',countSCONJ,'/NOUN: ',countNOUN,'/ADP: ',countADP,'/ADV: ',countADV,countall/2)

def transform_in_date(data):
    meses=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
    data=data.lower()
    if data == "amanhã":
        data = datetime.datetime.now().strftime("%d:%b")
    if data.find('dia')!=-1:
        dia=data[data.find('dia')+4:]
        dia=dia[:dia.find(' ')]
    else:
        dia=data[:data.find(' ')]
    if len(dia)==1:
        dia='0'+dia
    mes=data[data.find('de')+3:]
    if len(str(meses.index(mes)+1))==1:
        mes='0'+str(meses.index(mes)+1)
    else:
        mes=str(meses.index(mes)+1)
    ano=datetime.datetime.now().strftime('%Y')
    data=dia+'/'+mes+'/'+ano
    return data