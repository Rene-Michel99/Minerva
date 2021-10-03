from os import system,listdir,popen,path,getpid,getcwd
import os

def get_hardware_info():
    import psutil as util

    pct=util.sensors_battery()[0]
    disk=util.disk_usage('c:/')
    cpu=util.cpu_percent()
    cpu2=util.cpu_times_percent()

    return pct,disk,cpu,cpu2

def prt_screen():
    import pyautogui as pg
    pg.hotkey('win','prntscrn')

def get_battery():
    import psutil as util

    pct=util.sensors_battery()[0]
    return pct

def open_app(app):
    app = app.replace('abrir o','')
    app = app.replace('abra o','')
    app = app.replace('inicie o','')
    app = app.replace(' ','')
    cmd='start '+app
    print(cmd)
    x=system(cmd)
    return x

def search_yt(video):
    video=video.replace('buscar','')
    video=video.replace('busque','')
    video=video.replace('busca','')
    video=video.replace('procure','')
    video=video.replace('pesquise','')
    video=video.replace('no youtube','')
    print(video)
    cmd='start firefox "www.youtube.com/results?search_query='+video.replace(' ','+')+'"'
    system(cmd)

def printer(arquivo):
    import pyautogui as pg
    import time

    path='file:///C:/Users/REN%C3%8A%20MICHEL/Downloads/'+arquivo
    system('start firefox')
    time.sleep(3)

    pg.moveTo(747,51)
    pg.click()

    pg.write(path)
    time.sleep(5)
    pg.press('enter')

    time.sleep(5)
    pg.hotkey('ctrl','p')

    time.sleep(5)

    pg.press('enter')

def have_connection():
    import socket
    ip_teste=socket.gethostbyname(socket.gethostname())
    if ip_teste=='127.0.0.1':
        return 0
    else:
        return 1

def copia_para(item,root_path,second_path):
    lista=listdir(second_path)

    for i in range(len(lista)):
        lista[i]=lista[i].lower()

    if item.lower() not in lista:
        arquivo1=root_path+'/'+item
        arquivo2=second_path+'/'+item
        #path_to_remove='"C:\\Users\\RENÊ MICHEL\\Desktop\\'+item+'"'

        data=None
        arq=open(arquivo1,'r',encoding='utf-8')
        data=arq.read()
        arq.close()

        arq=open(arquivo2,'w',encoding='utf-8')
        arq.write(data)
        arq.close()

        print(arquivo1,'copiado para',arquivo2)

        #path_to_remove='"C:\\Users\\RENÊ MICHEL\\Desktop\\'+item+'"'
        path_to_remove='"C:'+arquivo1.replace('/','\\')+'"'
        system('del '+path_to_remove)


def copia_para_binary(item,root_path,second_path):
    lista=listdir(second_path)

    for i in range(len(lista)):
        lista[i]=lista[i].lower()

    if item.lower() not in lista:
        arquivo1=root_path+'/'+item
        arquivo2=second_path+'/'+item
        #path_to_remove='"C:\\Users\\RENÊ MICHEL\\Desktop\\'+item+'"'

        data=None
        arq=open(arquivo1,'rb')
        data=arq.read()
        arq.close()

        arq=open(arquivo2,'wb')
        arq.write(data)
        arq.close()

        print(arquivo1,'copiado para',arquivo2)

        #path_to_remove='"C:\\Users\\RENÊ MICHEL\\Desktop\\'+item+'"'
        path_to_remove='"C:'+arquivo1.replace('/','\\')+'"'
        system('del '+path_to_remove)

def verify_dependecies(path):
    arq=open(path,'r',encoding='utf-8')
    dependencies=[]
    for line in arq:
        if line.find('open(')!=-1:
            string=line[line.find('open(')+5:]
            string=string[:string.find(',')]
            dependencies.append(string.replace("'",""))
    return dependencies


def organize_desktop():
    path='/Users/RENÊ MICHEL/Desktop'
    second_path='/Users/RENÊ MICHEL/Desktop/Codigos/'
    lista=listdir(path)

    for item in lista:
        if item.find('.py')!=-1:
            print(item)
            x=verify_dependecies(path+'/'+item)
            if x!=[]:
                for arquivo in x:
                    copia_para(arquivo,path,second_path+'Python')
            copia_para(item,path,second_path+'Python')
        elif item.find('.R')!=-1:
            print(item)
            copia_para(item,path,second_path+'R')
        elif item.find('.c')!=-1:
            print(item)
            name=item[:item.find('.')]
            copia_para(item,path,second_path+'C')
            copia_para_binary(name+'.exe',path,second_path+'C')
            copia_para_binary(name+'.o',path,second_path+'C')
        elif item.find('.html')!=-1:
            print(item)
            copia_para(item,path,second_path+'HTML')


def organize_documents():
    path='/Users/RENÊ MICHEL/OneDrive/Documents'
    path_to_create='C:\\Users\\RENÊ MICHEL\\Onedrive\\Documents\\'
    lista=listdir(path)

    for item in lista:
        if item.lower().find('aula')!=-1 or item.lower().find('correção')!=-1 or item.lower().find('exercício')!=-1 or item.lower().find('lista')!=-1:
            print(item)
            copia_para_binary(item,path,path+'/'+'Faculdade')
        elif item.find('.docx')!=-1:
            name = "Documentos Word"
            if not name in lista:
                cmd='mkdir '+'"'+path_to_create+name+'"'
                system(cmd)                      #mkdir "C:\Users\RENÊ MICHEL\Onedrive\Documents\Caralho"
            copia_para_binary(item,path,path+'/'+name)
        elif item.find('.pdf')!=-1:
            name = "Documentos PDF"
            if not name in lista:
                cmd='mkdir '+'"'+path_to_create+name+'"'
                system(cmd)
            copia_para_binary(item,path,path+'/'+name)

def organize_downloads():
    path='/Users/RENÊ MICHEL/Downloads'
    path_to_imgs='/Users/RENÊ MICHEL/Pictures'
    path_to_documents='/Users/RENÊ MICHEL/OneDrive/Documents'

    lista=listdir(path)

    for item in lista:
        if item.lower().find('.png')!=-1 or item.lower().find('.jpg')!=-1 or item.lower().find('.jpeg')!=-1:
            copia_para_binary(item,path,path_to_imgs)
        elif item.lower().find('.docx')!=-1 or item.lower().find('.pdf')!=-1 or item.lower().find('.txt')!=-1:
            copia_para_binary(item,path,path_to_documents)

def get_performance():
    pid = getpid()
    res = popen('tasklist /FI "PID eq '+str(pid)+'"').read()

    res = res.split("\n")[3:]

    res = res[0]
    res = res.split()[4]

    res = res+" Kilobytes"
    return res

def organize_pasta():
    organize_desktop()
    organize_downloads()
    organize_documents()

def get_takList():
    res=popen('tasklist').read()
    copy=res.replace('Memory Compression','Memory_Compression')

    arq=open('saida.txt','w')
    arq.write(copy)
    arq.close()

    arq=open('saida.txt','r')
    lista=[]
    dic={}
    skip=0
    for i in arq:
        if skip>3 and i.find('Memory_Compression')==-1:
            name=''
            ident=''
            n_session=''
            session=''
            uso_m=''
            st=''
            for j in i:
                if j!=' ':
                    st+=j
                else:
                    if name=='' and st!=' ':
                        name=st
                    elif ident=='' and st!=' ':
                        ident=st
                    elif n_session=='' and st!=' ':
                        n_session=st
                    elif session=='' and st!=' ':
                        session=st
                    elif uso_m=='' and st!=' ':
                        uso_m=st
                    st=''
            dic['nome']=name
            dic['id']=int(ident)
            dic['nome_sesssao']=n_session
            dic['sessao']=int(session)
            dic['uso_memoria']=int(uso_m.replace('.',''))
            lista.append(dic)
            dic={}

        skip+=1
    arq.close()
    maior=0
    maior2=0
    maior3=0
    name=''
    name2=''
    name3=''
    for i in lista:
        if i['uso_memoria']>maior:
            maior=i['uso_memoria']
            name=i['nome']
        elif i['uso_memoria']>maior2:
            maior2=i['uso_memoria']
            name2=i['nome']
        elif i['uso_memoria']>maior3:
            maior3=i['uso_memoria']
            name3=i['nome']
    
    string='Os 3 progamas que mais estão usando da memória são '+name+' com '+str(maior)+'Kb, '+name2+' com '+str(maior2)+'Kb '+' e '+name3+' com '+str(maior3)+'Kb'
    return string

def busca(alvo,raiz,lista=[]):
    current_path=raiz
    next_path=listdir(current_path)
    if alvo in next_path or alvo.upper() in next_path or alvo.title() in next_path:
        #print(alvo)
        return current_path+'/'+alvo
    x=''
    for i in next_path:
        x=current_path+'/'+i
        if path.isdir(x) and i[0]!='.' and path.getsize(x)>0:
            try:
                x=busca(alvo,current_path+'/'+i)
                if x.find(alvo)!=-1 or x.find(alvo.title())!=-1 or x.find(alvo.upper())!=-1 or x.find(alvo).lower():
                    #return x
                    lista.append(x)
            except:
                x=''
    return lista


def search_local(alvo,auto_correct=True):
    if auto_correct:
        aux=alvo[::-1]
        aux=aux.replace(' .','.')
        aux=aux[:aux.find(' ')]
        alvo=aux[::-1]
    print(alvo)
    lista=listdir('c:/Users')
    lista.remove('All Users')
    lista.remove('Default')
    lista.remove('Default User')
    lista.remove('desktop.ini')
    lista.remove('Public')
    lista.remove('Todos os Usuários')
    lista.remove('Usuário Padrão')
    raiz='c:/Users/'+lista[1]
    res=busca(alvo,raiz)
    print(res)
    if res==None or res==[]:
        return 'Arquivo ou pasta não existe'
    else:
        path = res[::-1]
        path = path[path.find("/"):]
        path = path[::-1]
        #system('explorer start '+)
        return res

#DEIXAR UM DIA TESTANDO NO WIN7
#Para prevenção de vírus seria interessante buscar por nome também assim seria possível somar os Kb e identificar como travamento
class Manager:
    def __init__(self):
        import threading
        self.targets = []
        self.running = True
        self.processes_closed = []

        th = threading.Thread(target=self.inspect_processes)
        th.daemon = True
        th.start()

        self.handle_input()

    def handle_input(self):
        while self.running:
            cmd = input("Digite: ")
            if cmd=="shutdown":
                self.shutdown()
            elif cmd=="process_log":
                self.generate_log()
            elif cmd=="closed_log":
                self.view_closed_log()
    
    def view_closed_log(self):
        cmd = 'notepad "'+getcwd()+"\\"+"closed_log.txt"+'"'
        system(cmd)

    def shutdown(self):
        self.running = False
    
    def check_existence(self,pid):
        for i,process in enumerate(self.targets):
            if process["PID"]==pid:
                return i
        return -1
    
    def generate_log(self):
        arq = open("log.txt","w")
        for process in self.targets:
            arq.write(str(process)+"\n")
        arq.close()

        cmd = 'notepad "'+getcwd()+"\\"+"log.txt"+'"'
        system(cmd)
    
    def get_closeds(self):
        return self.processes_closed.copy()

    def inspect_processes(self):
        #Mais de um filtro
        #TASKLIST /FI "STATUS eq NOT RESPONDING" /FI "MEMUSAGE gt 300000"
        from time import sleep

        sys_list = ["Memory","System","Registry","SetupHost.exe"]

        changes = 0
        while self.running:
            tasks = popen('TASKLIST /FI "MEMUSAGE gt 250000"').read()
            #tasks = popen('TASKLIST /FI "MEMUSAGE gt 90000"').read()
            try:
                tasks = tasks.split("\n")[3:]
                tasks = tasks[0:len(tasks)-1]
            except:
                del (tasks)
                return []

            for task in tasks:
                task = task.split()
                check = self.check_existence(task[1])
                if task[0] in sys_list:
                    continue
                if check==-1:
                    self.targets.append({"NAME":task[0],"PID":task[1],"MEMUSAGE":task[4].replace(".",""),"DANGER":0})
                else:
                    if int(self.targets[check]["MEMUSAGE"])<int(task[4].replace(".",""))*1.5:
                        self.targets[check]["MEMUSAGE"] = int(task[4].replace(".",""))
                        self.targets[check]["DANGER"] += 1
                        changes += 1
                    elif int(self.targets[check]["MEMUSAGE"])>int(task[4].replace(".","")):
                        self.targets[check]["MEMUSAGE"] = int(task[4].replace(".",""))
                        self.targets[check]["DANGER"] -= 1

            sleep(150)
            if changes>0:
                self.kill_broken_process()
                changes = 0

            tasks = ""

    def kill_broken_process(self):
        to_remove = []
        arq = open("closed_log.text","a")
        for i,process in  enumerate(self.targets):
            if process["DANGER"]>3:
                #popen("TASKKILL /F /PID "+process["PID"])
                arq.write(str(process)+"\n")
                print("excluding ",process)
                to_remove.append(process)
                self.processes_closed.append(process["NAME"])
        arq.close()

        for item in to_remove:
            self.targets.remove(item)

