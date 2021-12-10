import datetime
import threading
import __init__
from Models import DBModel
from TasksController import Tasker
from Models import EngineVSTTModel
from Models import Sys_funcs
from Models import Web_scrapper
from Views import Interface
from ChatbotController import ChatbotController

class Minerva:
    def __init__(self):
        self.tasker = Tasker()
        self.engine_vstt = EngineVSTTModel()
        self.running = False
        self.exceptions_re = []
        self.Db = DBModel()
        self.engine_chat = ChatbotController()
        self.th_respose_tasks = []
        self.interface = Interface()
        self.permissions = {
            '<weather>':self.Db,
            '<lembrete>':[self.engine_vstt,self.Db]
        }

        
    def init_threads(self):
        #th = threading.Thread(target=self.thread_count_next_organize)
        #th.daemon = True
        #th.start()

        th2 = threading.Thread(target=self.manage)
        th2.setDaemon(True)
        th2.start()
    
    def thread_count_next_organize(self):
        from time import sleep
        while self.running:
            sleep(1800)
            Sys_funcs.organize_pasta()
            self.th_respose_tasks.append("Organizei as pastas")
    
    def find_tokens(self,inp):
        tokens = {
            "<temp>":Web_scrapper.get_only_temp,
            "<age>":self.Db.getAge,
            "<news>":self.tasker.get_news
        }
        
        inp = inp.replace(" ","* ")
        inp = inp.split()
        for i in range(len(inp)):
            word = inp[i].replace("*","")
            if word in tokens.keys()!=-1:
                inp[i] = str(tokens[word]()) + "*"
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
            resposta = self.tasker.call(resposta,res,pack)
            self.engine_vstt.speak(resposta)

    def change_input(self,*kwargs):
        if self.engine_vstt.how_get_input == 2:
            self.how_get_input = 1
        elif self.engine_vstt.how_get_input == 1:
            self.engine_vstthow_get_input = 2

    def finalizar(self,*kwargs):
        self.engine_vstt.speak('Tudo bem tenha uma ótima '+self.tasker.get_the_status(datetime.datetime.now().strftime("%H")))
        self.running = False
        self.engine_chat.have_to_learn()
        self.Db.update_last_shutdown(datetime.datetime.now().strftime("%d:%m:%Y"))
        self.interface.shutdown()
        return 0

    def get_th_responses(self):
        for item in self.tasker.th_respose_tasks:
            self.engine_vstt.speak(item)
        self.tasker.th_respose_tasks.clear()

    def interpreter(self):
        res = self.engine_vstt.take_command()
        if res == None:
            print('Error')
        else:
            res = res.lower()
            self.do(res)

    def analysis(self):
        pct_b,disk_u,cpu_d,cpu2 = Sys_funcs.get_hardware_info()
        text = self.tasker.structurize_data_hardware(pct_b,disk_u,cpu_d,cpu2)
        if text != None:
            self.engine_vstt.speak(text)
            
        print('Bateria: ',pct_b,'% Uso da memória: ',disk_u,' Uso da cpu: ',cpu2)
    
    def manage(self):
        from time import sleep

        while self.running:
            sleep(60*5)
            battery_lv = Sys_funcs.get_battery()
            if battery_lv == 100:
                self.engine_vstt.speak("Bateria totalmente carregada")
            elif battery_lv == 20:
                self.engine_vstt.speak("Bateria abaixo de 20 por cento")

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
        reminders = self.Db.find_in_reminders(data_hoje)

        if reminders != []:
            self.engine_vstt.speak('Você me pediu para te lembrar algumas coisas para hoje, vou listar,')
            for item in reminders:
                self.engine_vstt.speak(item[1])

    def wishme(self):
        string = self.tasker.get_the_status(datetime.datetime.now().strftime("%H"))
        if string.find('Noite')!=-1:
            string='Boa noite mestre'
        elif string.find('Tarde')!=-1:
            string='Boa tarde mestre'
        elif string.find('Manhã')!=-1:
            string='Bom dia mestre'
        
        self.engine_vstt.speak(string+', Bem vindo de volta')

    def initialize_voice_engine(self):
        act = Sys_funcs.have_connection()
        self.engine_vstt.set_interface_conn(self.interface)

        if not act:
            self.engine_vstt.speak('Não há conexão com a internet, reconhecimento de voz em português desativado')
            self.how_get_input = 2
        else:
            self.how_get_input = 2
            #self.update_weather_data()
        self.wishme()

    def initialize_interface(self):
        th = threading.Thread(target=self.interface.start)
        th.setDaemon(True)
        th.start()

    def start(self):
        self.running = True
        self.initialize_interface()

        self.initialize_voice_engine()
        #self.analysis()
        #self.verify_reminders()
        self.init_threads()

        while self.running:
            self.interpreter()
            if self.tasker.exceptions_re != []:
                x = self.tasker.status()
                self.engine_vstt.speak(x)
            if self.tasker.th_respose_tasks != []:
                self.get_th_responses()

minerva = Minerva()
minerva.start()

