import os
from mutagen.mp3 import MP3
import pygame
import threading
import time
import mutagen
from random import randint
from tkinter import *

class tela(object):
    def __init__(self,parent,prin):
        self.main=parent
        self.escolhe=''
        canvas = Canvas(parent)
        scroll_y = Scrollbar(parent, orient="vertical", command=canvas.yview)

        frame = Frame(canvas)
        # group of widgets
        self.index=[i for i in range(len(prin))]
        self.lis=[]
        for i,musica in enumerate(prin):
            st=str(i+1)+'.'+musica.nome+'\n'+musica.artist
            self.lis.append(Button(frame,text=st,width=50,height=5,command=lambda c=self.index[i]: self.escolher(c)))
            self.lis[i].pack()
        # put the frame in the canvas
        canvas.create_window(0, 0, anchor='nw', window=frame)
        # make sure everything is displayed before configuring the scrollregion
        canvas.update_idletasks()

        canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)
                         
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')
            
            
    def escolher(self,i):
        self.escolhe=i
        self.main.destroy()

class musicass():
    def __init__(self,album,nome,length,artist,genre,path):
        self.album=self.remove(album)
        self.nome=self.remove(nome)
        self.length=length
        self.artist=self.remove(artist)
        self.genre=self.remove(genre)
        self.path=path
        
    def remove(self,log):
        log=list(log)
        try:
            if log[0]==' ' and len(log)>1:
                log[0]=''
        except:
            pass
        res=''
        for i in log:
            if i!='[' and i!=']':
                res=res+i
        return res.title()

def retorna_dados(info):
    pos=''
    data=''
    block=False
    tup=[]
    indicators=[]
    ind=''
    for i in range(len(info)): #constroi uma tupla de indicadores usando else
        pos=info[i]
        if pos=='[':
            block=True
            indicators.append(ind)
            ind=''
        if block:
            data=data+pos
        if pos==']':
            block=False
            tup.append(data)
            data=''
        elif not block:
            ind=ind+pos
    res1=adequa(tup)
    res2=adequa(indicators)
    return tup,indicators

def adequa(indicators):
    for i in range(len(indicators)):
        if indicators[i].find(',')!=-1:
            ind=indicators[i]
            j=ind.find(',')
            ind=list(ind)
            ind[j]=''
            ind=''.join(ind)
            indicators[i]=ind
        if indicators[i].find('{')!=-1:
            ind=indicators[i]
            j=ind.find('{')
            ind=list(ind)
            ind[j]=''
            ind=''.join(ind)
            indicators[i]=ind
        if indicators[i].find(':')!=-1:
            ind=indicators[i]
            j=ind.find('{')
            ind=list(ind)
            ind[j]=''
            ind=''.join(ind)
            indicators[i]=ind
        if indicators[i].find("'")!=-1:
            ind=indicators[i]
            j=ind.find("'")
            ind=list(ind)
            ind[j]=''
            ind=''.join(ind)
            indicators[i]=ind
        if indicators[i].find("'")!=-1:
            ind=indicators[i]
            j=ind.find("'")
            ind=list(ind)
            ind[j]=''
            ind=''.join(ind)
            indicators[i]=ind
            indicators[i]=ind

def define_arq():
    arquivos=[]
    pasta=os.listdir('/Users/RENÊ MICHEL/Music/')
    for i in pasta:
        if i.endswith('.mp3'):
            arquivos.append(i)
    return arquivos

def conserta_string(st):
    st=list(st)
    res=''
    for i in st:
        if i>=' ' and i<='~':
            res=res+i
    return res

def remove(log):
        log=list(log)
        res=''
        for i in log:
            if i!='[' and i!=']':
                res=res+i
        return res

def conserta(dado1,dado2): #tup[nome],musics[i]
    dado1=dado1.replace('"','')
    dado1=remove(dado1)
    if 'tumblr' in dado1 or 'Lavf' in dado1 or 'Tumblr' in dado1 or '0.72' in dado1:
        return dado2.title()
    if dado1.isnumeric():
        return dado2.title()
    if dado2.find(dado1)!=-1 and dado1.find(dado2)==-1: #ultima mudança
        return dado2.title()
    else:
        return dado1.title()

def tira_coisa(string):
    if string.find('[Audio]')!=-1:
        string=string.replace('[Audio]','')
    if string.find('(Lyrics)')!=-1:
        string=string.replace('(Lyrics)','')
    if string.find('[Hd]')!=-1:
        string=string.replace('[Hd]','')
    if string.find('(Lyric Video)')!=-1:
        string=string.replace('(Lyric Video)','')
    if string.find('(Official Audio)')!=-1:
        string=string.replace('(Official Audio)','')
    if string.find('(Official Video)')!=-1:
        string=string.replace('(Official Video)','')
    if string.find('(Lyrics Video)')!=-1:
        string=string.replace('(Lyrics Video)','')
    #print('string:',string)
    return string

def transform(nome):
    #print('primeiro:',nome)
    mid=nome.find('-')
    nome=nome.title()
    nome=tira_coisa(nome)
    log=nome.find('.Mp3')
    #print('primeiro:',nome)
    music=nome[mid+1:log]
    artist=nome[:mid]
    if music[0]==' ':
        music=music[1:]
    elif music[0]==' ' and music[1]==' ':
        music=music[2:]
    #print('musica:',music)
    #print('artista:',artist)
    return music,artist

def get_def(string):
    string=tira_coisa(string)
    mid=string.find('-')
    end=string.find('(')
    artista=string[:mid]
    musica=string[mid+1:end]
    resto=string[end:]
    album=''
    genero=''
    resto=list(resto)
    block=False
    block2=False
    for i in range(len(resto)):
        if resto[i]=='(':
            block=True
        if resto[i]==')':
            block=False
        if resto[i]=='[':
            block2=True
        if resto[i]==']':
            block2=False
        if block2:
            genero=genero+resto[i]
        if block:
            album=album+resto[i]
    try:
        album=list(album)
        album[0]=''
        album=''.join(album)
    except:
        album='?'
    try:
        genero=list(genero)
        genero[0]=''
        genero=''.join(genero)
    except:
        genero='?'
    print(artista,'-',musica,'-',album,'-',genero)

def get_length(path):
    suiz=path
    st=MP3(suiz)
    absol=divmod(st.info.length,60)
    duration=absol[0]+(absol[1]/100)
    duration*=60
    return duration
    #print('tempo:',self.duration)
    
def create_arq():
    musics=define_arq()
    path='/Users/RENÊ MICHEL/Music/'
    dados=''
    arq=open('metadados.txt','w')
    classes=[]
    pos=''
    for i in range(len(musics)):
        musica=path+musics[i]
        copy=musica
        info=mutagen.mp3.EasyMP3(musica).tags
        fu=str(info)
        #print('{\n')
        dados=dados+'{\n'
        #print(fu)
        dados=dados+fu
        #print('(',musics[i],')')
        x=conserta_string(musics[i])
        dados=dados+'('+x+')'
        tup,indicators=retorna_dados(fu)
        try:
            album=indicators.index('album:')
        except:
            album=-1
        try:
            nome=indicators.index(' title:')
        except:
            try:
                nome=indicators.index(" title':")
            except:
                nome=-1
        length=0
        try:
            artist=indicators.index(' artist')
        except:
            try:
                artist=indicators.index(' albumartist:')
            except:
                artist=-1
        try:
            genre=indicators.index(' genre:')
        except:
            genre=-1
            
        if len(tup)>0: #o tira coisa foi chamado aqui
            fs=conserta(tup[nome],musics[i]) #chama transform pro segundo
            length=get_length(copy)
            pos=musicass(tup[album],tira_coisa(fs),length,tup[artist],tup[genre],copy)
        else:
            if musics[i].find('-')!=-1:
                nameM,cantor=transform(musics[i])
                #get_def(musics[i])
                length=get_length(copy)
                pos=musicass('?',nameM,length,cantor,'?',copy)
            else:
                length=get_length(copy)
                pos=musicass('?',musics[i],length,'?','?',copy) 
        classes.append(pos)
        dados=dados+str(indicators)+str(tup)
        dados=dados+'}\n'
        #print('}\n')
        try:
            arq.write(dados)
        except:
            x=conserta_string(dados)
            arq.write(x)
        dados=''
    arq.close()
    return classes    
        
def split(input_list):
    input_list_len = len(input_list)
    midpoint = input_list_len // 2
    return input_list[:midpoint], input_list[midpoint:]

def merge_sorted_lists(list_left, list_right):
    if len(list_left) == 0:
        return list_right
    elif len(list_right) == 0:
        return list_left
    index_left = index_right = 0
    list_merged = []  
    list_len_target = len(list_left) + len(list_right)
    while len(list_merged) < list_len_target:
        if list_left[index_left].nome <= list_right[index_right].nome:
            list_merged.append(list_left[index_left])
            index_left += 1
        else:
            list_merged.append(list_right[index_right])
            index_right += 1
        if index_right == len(list_right):
            list_merged += list_left[index_left:]
            break
        elif index_left == len(list_left):
            list_merged += list_right[index_right:]
            break
    return list_merged

def merge_sort(input_list):
    if len(input_list) <= 1:
        return input_list
    else:
        left, right = split(input_list)
        return merge_sorted_lists(merge_sort(left), merge_sort(right))

class Player:
    def __init__(self):
        self.all_musics=merge_sort(create_arq())
        self.cont=0
        self.opt=''
        self.choose=None
        self.run=True
        th=threading.Thread(target=self.tocar)
        th.daemon=True
        th.start()

    def next(self):
        self.cont+=1
        self.opt='next'

    def previous(self):
        self.cont-=1
        self.opt='previous'

    def pause(self):
        self.opt='pause'

    def show_all_musics(self):
        self.opt='change'
        root=Tk()
        self.choose=tela(root,self.all_musics)
        root.mainloop()

    def escolhe(self):
        x=self.choose.escolhe
        return x

    def unpause(self):
        self.opt='unpause'
        
    def tocar(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.all_musics[self.cont].path)
        pygame.mixer.music.play()
        
        while self.run:

            if self.opt=='next':
                pygame.mixer.music.load(self.all_musics[self.cont].path)
                pygame.mixer.music.play()
                self.opt='none'
            elif self.opt=='pause':
                pygame.mixer.music.pause()
                self.opt='none'
            elif self.opt=='previous':
                pygame.mixer.music.load(self.all_musics[self.cont].path)
                pygame.mixer.music.play()
                self.opt='none'
            elif self.opt=='unpause':
                pygame.mixer.music.unpause()
                self.opt='none'
            elif self.opt=='change' and self.choose!=None:
                x=self.escolhe()
                if x!='':
                    pygame.mixer.music.load(self.all_musics[x].path)
                    pygame.mixer.music.play()
                    self.opt='none'
                    self.choose=None
            elif not pygame.mixer.music.get_busy():
                self.next()


            

