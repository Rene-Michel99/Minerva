import datetime
import threading
from Pipe_chat import Chatbot
#from Modules import MinervaDB
from Modules.Tasker import Core
from Modules.EngineVSTT import EngineVSTT
from Modules import Aux_functions
from Modules import Sys_funcs
from Modules import Web_scrapper


class Minerva:
    def __init__(self):
        self.tasker = Core()
        self.engine_vstt = EngineVSTT()
        self.running = True
        self.exceptions_re = []
        #self.Db = MinervaDB.DB()
        self.engine_chat = Chatbot()
        self.th_res_tasks = []
        self.permissions = {
            '<weather>':self.Db,'<lembrete>':[self.engine_vstt,self.Db]
        }

        th = threading.Thread(target=self.thread_count_next_organize)
        th.daemon = True
        #th.start()
    
    def thread_count_next_organize(self):
        from time import sleep
        while self.running:
            sleep(1800)
            Sys_funcs.organize_pasta()
            self.th_res_tasks.append("Organizei as pastas")
    
    def find_tokens(self,inp):
        tokens = {"<temp>":Web_scrapper.get_only_temp,"<age>":self.Db.getAge,"<news>":self.tasker.get_news}
        inp = inp.replace(" ","* ")
        inp = inp.split()
        for i in range(len(inp)):
            word = inp[i].replace("*","")
            if word in tokens.keys()!=-1:
                inp[i] = tokens[word]() + "*"
        inp = "".join(inp)
        inp = inp.replace("*"," ")
        return inp
    
    def need_permissions(self,func):
        if func in self.permissions:
            return self.permissions[func]
        else:
            return False

    def do(self,res):
        resposta = self.engine_chat.chat(res)

        if resposta == "<finalizar>":
            self.finalizar()
        elif resposta not in self.tasker.dic_funcs:
            resposta = self.find_tokens(resposta)
            self.engine_vstt.speak(resposta)
        elif resposta != 0:
            pack = self.need_permissions(resposta)
            resposta = self.tasker.do(resposta,res,pack)
            self.engine_vstt.speak(resposta)

    def change_input(self,*kwargs):
        if self.engine_vstt.how_get_input==2:
            self.how_get_input = 1
        elif self.engine_vstt.how_get_input==1:
            self.engine_vstthow_get_input = 2

    def finalizar(self,*kwargs):
        self.engine_vstt.speak('Tudo bem tenha uma ótima '+Aux_functions.get_the_status(datetime.datetime.now().strftime("%H")))
        self.running = False
        self.engine_chat.have_to_learn()
        self.Db.update_last_shutdown(datetime.datetime.now().strftime("%d:%m:%Y"))
        return 0

    def get_th_responses(self):
        for item in self.tasker.th_res_tasks:
            self.engine_vstt.speak(item)
        self.tasker.th_res_tasks.clear()

    def interpreter(self):
        res = self.engine_vstt.take_command()
        if res == None:
            print('Error')
        else:
            res = res.lower()
            res2 = ''
            if res.find('minerva') != -1:
                if res == 'minerva':
                    self.engine_vstt.speak('Estou te ouvindo')
                    res = self.engine_vstt.take_command()
                else:
                    res = res[res.find('minerva')+len('minerva')+1:]

                if res.find('depois')!=-1:
                    res2=res[res.find('depois')+7:]
                    res=res[:res.find(' depois')]
                
                self.do(res)
                if res2 != '':
                    self.do(res2)
            elif self.how_get_input == 2:
                self.do(res)

    def analysis(self):
        pct_b,disk_u,cpu_d,cpu2=Sys_funcs.get_hardware_info()
        x=0
        if pct_b<=20 or disk_u.percent>80 or cpu_d>75:
            self.engine_vstt.speak('Tomei a liberdade de analisar um pouco o hardware')
        if pct_b<=20:
            x+=1
            self.engine_vstt.speak('A bateria se encontra em'+str(pct_b)+'% , sujiro que coloque para carregar')
        if disk_u.percent>80:
            x+=1
            self.engine_vstt.speak('Mais de'+str(round(disk_u.percent))+'%'+' da memória principal está em uso, posso deletar algumas coisas caso desejar')
        if cpu_d>75:
            x+=1
            self.engine_vstt.speak('A cpu está sendo bastante usada, o valor atual é de'+str(cpu_d)+', posso dar um jeito nisso')
        if x>0:
            self.engine_vstt.speak('Vou imprimir na tela caso queira copiar esses dados')
            print('Bateria: ',pct_b,'% Uso da memória: ',disk_u,' Uso da cpu: ',cpu2)
    
    def manage(self):
        if Sys_funcs.get_battery() == 100:
            self.engine_vstt.speak("Bateria totalmente carregada")

    def update_weather_data(self):
        updated = self.Db.get_last_upadte_weather()
        date_now = datetime.datetime.now().strftime('%d:%m')
        if Sys_funcs.have_connection() and updated==None or updated!=date_now:
            print(date_now,updated)
            data = Web_scrapper.get_weather(Web_scrapper.get_city(),more=True)
            self.Db.insert_in_weather(data,date_now)
        else:
            print('Nothing to update')

    def verify_reminders(self):
        data_hoje = datetime.datetime.now().strftime('%d:%m:%Y').replace(':','/')
        descrs = self.Db.find_in_reminders(data_hoje)
        if type(descrs)==list:
            self.engine_vstt.speak('Você me pediu para te lembrar algumas coisas para hoje, vou citar,')
            for item in descrs:
                self.engine_vstt.speak(item)
            self.Db.delete_in_reminders(data_hoje)
        del(data_hoje,descrs)

    def wishme(self):
        string = Aux_functions.get_the_status(datetime.datetime.now().strftime("%H"))
        if string.find('Noite')!=-1:
            string='Boa noite mestre'
        elif string.find('Tarde')!=-1:
            string='Boa tarde mestre'
        elif string.find('Manhã')!=-1:
            string='Bom dia mestre'
        self.engine_vstt.speak(string+', Bem vindo de volta')

    def initialize_voice_engine(self):
        act = Sys_funcs.have_connection()
        if not act:
            self.engine_vstt.speak('Não há conexão com a internet, reconhecimento de voz em português desativado, você deve falar em inglês')
            self.how_get_input = 2
        else:
            self.how_get_input = 2
            #self.update_weather_data()
        del(act)
        self.wishme()

    def start(self):
        self.initialize_voice_engine()    

        self.analysis()
        
        #self.verify_reminders()

        while self.running:
            self.manage()
            self.interpreter()
            if self.tasker.exceptions_re != []:
                x = self.tasker.status()
                self.engine_vstt.speak(x)
            if self.tasker.th_res_tasks != []:
                self.get_th_responses()

minerva = Minerva()
minerva.start()

