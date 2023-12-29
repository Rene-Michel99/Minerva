import datetime
import threading
from ChatbotController import ChatbotController
from Models import DBModel
from TasksController import TasksController
from Views import EngineVSTTView
from Models import Web_scrapper


class Minerva:
    def __init__(self):
        super().__init__()
        self.tasks_controller = TasksController()
        self.interface_view = EngineVSTTView()
        self.RUNNING = False
        self.exceptions_re = []
        self.db_model = DBModel()
        self.engine_chat = ChatbotController()
        self.th_respose_tasks = []
    
    def load_permissions(self):
        self.permissions = {
            '<weather>': self.db_model,
            '<lembrete>': [self.interface_view,self.db_model]
        }

    def load_components(self):
        self.COMPONENTS = {
            "View": self.interface_view,
            "TTS": self.interface_view
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
        while self.RUNNING:
            sleep(1800)
            #self.tasks_controller.organize_pasta()
            self.th_respose_tasks.append("Organizei as pastas")
    
    def find_tokens(self,inp):
        tokens = {
            "<temp>":Web_scrapper.get_only_temp,
            "<age>":self.db_model.getAge,
            "<news>":self.tasks_controller.get_news
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
        elif resposta not in self.tasks_controller.switcher:
            resposta = self.find_tokens(resposta)
            self.interface_view.speak(resposta)
        elif resposta != 0:
            pack = self.need_permissions(resposta)
            resposta = self.tasks_controller.call(resposta,res,pack)
            self.interface_view.speak(resposta)

    def change_input(self,*kwargs):
        if self.interface_view.how_get_input == 2:
            self.how_get_input = 1
        elif self.interface_view.how_get_input == 1:
            self.interface_viewhow_get_input = 2

    def finalizar(self,*kwargs):
        self.interface_view.speak('Tudo bem tenha uma ótima '+self.tasks_controller.get_the_status(datetime.datetime.now().strftime("%H")))
        self.RUNNING = False
        self.engine_chat.have_to_learn()
        self.db_model.update_last_shutdown(datetime.datetime.now().strftime("%d:%m:%Y"))
        self.interface_view.shutdown()
        return 0

    def get_th_responses(self):
        for item in self.tasks_controller.th_respose_tasks:
            self.interface_view.speak(item)
        self.tasks_controller.th_respose_tasks.clear()

    def interpreter(self):
        res = self.interface_view.take_command()
        if res == None:
            print('Error')
        else:
            res = res.lower()
            self.do(res)

    def analysis(self):
        pct_b,disk_u,cpu_d,cpu2 = self.tasks_controller.get_hardware_info()
        text = self.tasks_controller.structurize_data_hardware(pct_b,disk_u,cpu_d,cpu2)
        if text != None:
            self.interface_view.speak(text)
            
        print('Bateria: ',pct_b,'% Uso da memória: ',disk_u,' Uso da cpu: ',cpu2)
    
    def manage(self):
        from time import sleep

        while self.RUNNING:
            sleep(60*5)
            battery_lv = self.tasks_controller.get_battery()
            if battery_lv == 100:
                self.interface_view.speak("Bateria totalmente carregada")
            elif battery_lv == 20:
                self.interface_view.speak("Bateria abaixo de 20 por cento")

    def update_weather_data(self):
        updated = self.db_model.get_last_upadte_weather()
        date_now = datetime.datetime.now().strftime('%d:%m')

        if self.tasks_controller.have_connection() and updated==None or updated!=date_now:
            print(date_now,updated)
            data = Web_scrapper.get_weather(Web_scrapper.get_city(),more=True)
            self.db_model.insert_in_weather(data,date_now)
        else:
            print('Nothing to update')

    def verify_reminders(self):
        data_hoje = datetime.datetime.now().strftime('%d:%m:%Y').replace(':','/')
        reminders = self.db_model.find_in_reminders(data_hoje)

        if reminders != []:
            self.interface_view.speak('Você me pediu para te lembrar algumas coisas para hoje, vou listar,')
            for item in reminders:
                self.interface_view.speak(item[1])

    def wishme(self):
        string = self.tasks_controller.get_the_status(datetime.datetime.now().strftime("%H"))
        if string.find('Noite')!=-1:
            string='Boa noite mestre'
        elif string.find('Tarde')!=-1:
            string='Boa tarde mestre'
        elif string.find('Manhã')!=-1:
            string='Bom dia mestre'
        
        self.interface_view.speak(string+', Bem vindo de volta')

    def initialize_voice_engine(self):
        status_conn = self.tasks_controller.have_connection()

        if not status_conn:
            self.interface_view.speak('Não há conexão com a internet, reconhecimento de voz em português desativado')
            self.how_get_input = 2
        else:
            self.how_get_input = 2
            #self.update_weather_data()
        self.wishme()

    def initialize_interface(self):
        th = threading.Thread(target=self.interface_view.start)
        th.setDaemon(True)
        th.start()

    def start(self):
        self.load_components()
        self.load_permissions()
        self.RUNNING = True
        self.init_threads()
        self.initialize_interface()

        self.initialize_voice_engine()
        #self.analysis()
        #self.verify_reminders()

        while self.RUNNING:
            self.interpreter()
            if self.tasks_controller.exceptions_re != []:
                x = self.tasks_controller.status()
                self.interface_view.speak(x)
            if self.tasks_controller.th_respose_tasks != []:
                self.get_th_responses()

minerva = Minerva()
minerva.start()

