from selenium import webdriver
import threading
import time
from Pipe_chat import Chatbot

class Whatsapp_Framework:
    def __init__(self):
        self.list_contatos=[]
        self.running=True
        self.timeout = False
        self.greetings = "Olá meu mestre no momento se encontra ocupado, porém caso queira pedir algo ou informar algo posso tratar isso então fique a vontade para falar :)"
        self.ignore_msgs = ["Trabalho de Redes - 16/09","Pesca Remota-Links na des","Cabaré sem Pyta🐧"]

        self.bot = Chatbot()
        options=webdriver.FirefoxOptions()
        options.add_argument('lang=pt-br')
        self.driver=webdriver.Firefox(executable_path=r'./geckodriver.exe')

        self.auto_pillot()
        
    def set_contacts(self):
        self.list_contatos.clear()
        contatos=self.driver.find_elements_by_xpath('//div[@class="_2kHpK"]')
        self.list_contatos=[]
        for contato in contatos:
            children=[]
            children=contato.find_elements_by_xpath('.//*')
            d_cont={}
            new=False
            block=False
            for child in children:
                if child.get_attribute('class')=='_3ko75 _5h6Y_ _3Whw5' and not block:
                    name=child.get_property('title')
                    d_cont['name']=name
                    d_cont['element']=child
                    block=True
                elif child.get_attribute('class')=='_2iq-U':
                    msg=str(child.get_attribute('title')).replace('\u202a','')
                    msg=msg.replace('\u202c','')
                    d_cont['last_message']=msg
                elif child.get_attribute('class')=='_31gEB':
                    new=True
                    d_cont['is_new_msg']=child.get_attribute('innerHTML')
            if not new:
                d_cont['is_new_msg']=False
            self.list_contatos.append(d_cont)

    def get_contact(self,contato):
        for item in self.list_contatos:
            if contato==item['name']:
                return item['element']

    def get_msg(self,name):
        classe='copyable-text'
        conversa=[]
        already_searched=[]
        time.sleep(3)
        try:
            conv_Data=self.driver.find_elements_by_xpath(f"//div[@class='{classe}']")
            for msg in conv_Data:
                if str(msg.get_attribute('data-pre-plain-text')).find(name)!=-1:
                    param=str(msg.get_attribute('data-pre-plain-text'))
                    if param not in already_searched:
                        x=self.driver.find_elements_by_xpath(f"//div[@data-pre-plain-text='{param}']")
                        for item in x:
                            y=item.find_element_by_xpath('..')
                            string=str(y.get_attribute('innerHTML'))
                            string=string[string.find('<span>')+6:]
                            string=string[:string.find('</')]
                            if conversa.count((string,param))==0:
                                conversa.append((string,param))
                        already_searched.append(param)

            for msg in conversa:
                print(msg)

            return conversa
        except:
            return []
    
    def send_msg(self,msg): #_3FRCZ copyable-text selectable-text
        time.sleep(3)
        chat_box=self.driver.find_elements_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]')
        chat_box[1].click()
        chat_box[1].send_keys(msg)
        time.sleep(3)
        sender=self.driver.find_element_by_xpath('//button[@class="_1U1xa"]')
        sender.click()

    def handle_new_msgs(self):
        for item in self.list_contatos:
            if item['is_new_msg'] and item['name'] not in self.ignore_msgs:
                name=item['name']
                print(name)
                element=item['element']
                item['is_new_msg']=False
                return name,element
        return None,None

    def initialize(self):
        while self.list_contatos==[]:
            try:
                self.set_contacts()
            except:
                pass
        print('Inicializado')

    def clock(self):
        time.sleep(120)
        self.timeout = True

    def setTimeOut(self):
        self.timeout = False
        th = threading.Thread(target=self.clock)
        th.daemon = True
        th.start()

    def chatting(self,element,contato):
        element.click()
        msg_to = self.greetings
        self.send_msg(msg_to)
        self.setTimeOut()

        while not self.timeout:
            msg_from = self.get_msg(contato+":")
            if msg_from!=[]:
                print(msg_from)
                msg_to = self.bot.chat(msg_from)
                self.send_msg(msg_to)

    def auto_pillot(self):
        self.driver.get('https://web.whatsapp.com/')
        self.initialize()

        while self.running:
            contato,element=self.handle_new_msgs()
            if contato!=None:
                self.chatting(element,contato)
            self.set_contacts()

    def chat(self,msg,contato):
        x=self.get_contact(contato)
        x.click()
        
        conversas=self.get_msg(contato+':')
        if conversas!=[]:
            NotImplemented
        self.send_msg(msg)
        

messenger=Whatsapp_Framework()
#messenger.conversar('Uma mensagem','+55 84 9671-6454')