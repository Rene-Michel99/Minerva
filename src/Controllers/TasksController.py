import datetime
import threading
import __init__
from Models import System_funcs
from Models import Web_scrapper
from Models import Manage_erros
from Models import Manage_erros
from Models import Utils

'''
{'time':self.time,'date':self.date,'get_errors':self.get_errors,'note':self.note,'g_tasks':self.g_tasks,
        'change_input':self.change_input,'status':self.status,
        'screen_cpt':self.screen_cpt,'scan_img':self.scan_img,'play_music':self.pause_music,'next_music':self.next_music,
        'previous_music':self.previous_music,'pause_music':self.pause_music,'unpause_music':self.unpause_music,'change_music':self.change_music,
        'battery':self.battery,'lembrete':self.lembrete,'finalizar':self.finalizar,'manage_expenses':self.manage_expenses,
        'math':self.math,'s_local':self.s_local,'s_yt':self.s_yt,'open':self.open,'s_zoom':self.s_zoom,'s_wiki':self.s_wiki,
        'weather':self.weather}'''

class Tasker(Utils):
    def __init__(self):
        super().__init__()
        self.exceptions_re = []
        self.th_respose_tasks = []
        self.occupied = []
        self.dic_funcs = {
            '<time>':self.time,
            '<date>':self.date,
            '<get_errors>':self.status,
            '<math>':self.math,
            '<s_yt>':self.open_youtube,
            '<open>':self.open_app,
            '<news>':self.get_news,
            '<s_zoom>':self.search_zoom,
            '<g_tasks>':self.g_tasks,
            '<screen_cpt>':self.screen_cpt,
            '<next_music>':self.next_music,
            '<battery>':self.get_battery,
            '<lembrete>':self.create_reminder,
            '<get_ocupied>':self.get_ocupied,
            '<get_performance>':self.get_performance,
            '<weather>':self.get_weather,
            '<s_wiki>':self.search_wiki,
            '<s_local>':self.search_local
            }

    def call(self,func,*kwargs):
        resposta = self.dic_funcs[func](*kwargs)
        return resposta
        
    def time(self,*kwargs):
        time = datetime.datetime.now().strftime("%H:%M")
        st = self.get_the_status(time[0:2])

        time = datetime.datetime.now().strftime("%I:%M")
        time = 'São '+time+', da '+st
        return time
    
    def date(self,*kwargs):
        string = self.translate(datetime.datetime.now().strftime("%A:%d:%b"))
        return string

    def status(self,*kwargs):
        string = ""
        if Manage_erros.errors==[]:
            string = 'Nenhum erro foi detectado'
        else:
            string = 'Encontrei alguns erros, vou citar'
            for error in Manage_erros.errors:
                erro = str(error)
                string += 'Na função '+erro
                print(erro)
                self.exceptions_re.append(error)
            Manage_erros.clean_list()
        return string

    @Manage_erros.get_error
    def math(self,*kwargs):
        res = kwargs[0]
        resp = 'O resultado é '+str(self.solve_math(res))
        return resp

    @Manage_erros.get_error
    def open_youtube(self,*kwargs):
        res = kwargs[0]
        res = res[res.find('youtube')+7:]
        Sys_funcs.search_yt(res)
        st = "Abrindo o youtube"
        return st
    
    def open_app(self,*kwargs):
        res = kwargs[0]
        x = Sys_funcs.open_app(res)
        resp = ""
        if x == 1:
            resp = 'Ocorreu um erro ao abrir '+res.replace('abrir','')
        else:
            resp = 'Abrindo '+res.replace('abrir','')
        return resp

    def get_news(self,*kwargs):
        from fuzzywuzzy import fuzz
        news = Web_scrapper.get_news()
        text = ""
        if news!=[]:
            if len(news)>15:
                news = news[:20]
            ant = ""
            for w in news:
                if ant!="" and fuzz.ratio(ant,w)<=55:                    
                    text += w+","
                ant = w
            text += "Isso foi tudo o que achei" 
            return text
        else:
            return "não consegui encontrar nenhuma notícia"

    @Manage_erros.get_error
    def search_zoom(self,*kwargs):
        res = kwargs[0]
        voice = kwargs[1]
        x = ''
        if res.find('de um ')!=-1:
            x = res[res.find('de um ')+6:]
        elif res.find(' o ')!=-1:
            x = res[res.find(' o ')+3:]

        voice.speak('Pesquisando preços de '+x)
        res = Web_scrapper.get_prices(x)
        res = self.three_more_cheap(res)
        print(res)
        return res

    @Manage_erros.get_error
    def g_tasks(self,*kwargs):
        import pyautogui as pg

        pg.hotkey('ctrl','shift','esc')
        return "Abrindo o gerenciador de tarefas"

    def screen_cpt(self,*kwargs):
        Sys_funcs.prt_screen()
        return "Captura de tela feita com sucesso"

    def next_music(self):
        import pyautogui as pg

        pg.press('nexttrack')
        return "Feito"

    def pause_music(self):
        import pyautogui as pg

        pg.press('playpause')
        return "Feito"

    def get_battery(self,*kwargs):
        x = str(Sys_funcs.get_battery())
        resp = 'O nível da bateria está em '+x+'%'
        return resp

    def create_reminder(self,*kwargs):
        engine_vstt = kwargs[1][0]
        Db = kwargs[1][1]

        engine_vstt.speak('O que eu devo te lembrar')
        lembrete = engine_vstt.take_command()
        engine_vstt.speak('Para que dia')
        data = engine_vstt.confirm()
        data = self.transform_in_date(data)
        Db.insert_in_reminders(data,lembrete)

        return 'Lembrete salvo com sucesso'

    def get_ocupied(self,*kwargs):
        res = ""
        if len(self.occupied) == 1:
            res = "Estou "+self.ocupied[0]
        elif len(self.occupied)>1:
            res = "Estou fazendo as seguintes tarefas "
            for item in self.occupied:
                res += ","+item
        else:
            res = "No momento nada"
        return res
    
    def get_performance(self,*kwargs):
        res = Sys_funcs.get_performance()
        res = "O uso da memória é de "+res
        return res
    
    @Manage_erros.get_error
    def get_weather(self,*kwargs):
        res = kwargs[0]
        Db = kwargs[1]
        print(res)
        response = ""
        if res.find('amanhã')!=-1:
            dia = int(datetime.datetime.now().strftime("%d"))+1
            x = Db.get_next_weather(str(dia))
            response = x['dia']+' pode ter '+x['clima']+' com '+x['máxima-mínima']+' e com '+x['prob_chuva']
        elif res.find('0')!=-1 or res.find('1')!=-1 or res.find('2')!=-1 or res.find('3')!=-1:
            dia = res[res.find('dia')+4:]
            x = Db.get_next_weather(dia)
            response = x['dia']+' pode ter '+x['clima']+' com '+x['máxima-mínima']+' e com '+x['prob_chuva']
        else:
            city = ""
            if res.find(" de ")!=-1:
                city = res[res.find(" de ")+4:]
            elif res.find(" em ")!=-1:
                city = res[res.find(" em ")+4:]
            else:
                city = Web_scrapper.get_city()
            response = Web_scrapper.get_weather(city)
        return response

    @Manage_erros.get_error
    def th_swiki(self,res):
        self.occupied.append('Pesquisando sobre '+res)
        x = Web_scrapper.get_on_wiki(res)

        x = "Encontrei algo sobre o que você queria saber, "+x+", Armazenei todo o resultado da pesquisa em um arquivo com o mesmo nome da pesquisa"
        self.th_respose_tasks.append(x)

        self.occupied.remove("Pesquisando sobre "+res)

    def search_wiki(self,*kwargs):
        res = kwargs[0]
        res = res[res.find('sobre ')+6:]
        response = 'Pesquisando sobre '+res+", isso pode demorar um tempo mas posso lhe responder outras coisas até terminar essa pesquisa"
        
        th = threading.Thread(target=self.th_swiki,args=(res,))
        th.daemon = True
        th.start()

        return response

    @Manage_erros.get_error
    def th_slocal(self,res):
        self.occupied.append("Buscando arquivo")
        x = Sys_funcs.search_local(res)
        if type(x)==str:
            pass
        else:
            x = "Encontrei o arquivo solicitado, ele se encontra em "+str(x) 
            self.th_respose_tasks.append(x)
        self.occupied.remove("Buscando arquivo")

    def search_local(self,*kwargs):
        res = kwargs[0]
        response = 'Este comando pode levar bastante tempo'

        th = threading.Thread(target=self.th_slocal,args=(res,))
        th.daemon = True
        th.start()

        return response
    
    @Manage_erros.get_error
    def autoPillot(self,*kwargs):
        NotImplemented


tasker = Tasker()