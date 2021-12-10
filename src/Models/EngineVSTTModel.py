import speech_recognition as sr
from os import popen
from pygame import mixer
#from pocketsphinx import LiveSpeech
#for phrase in LiveSpeech(): print(phrase)

class EngineVSTTModel:
    def __init__(self):
        self.cmd = 'spd-say -o "rhvoice" -w -t female1 '
        self.how_get_input = 2
        self.interface = None

    def set_interface_conn(self,interface):
        self.interface = interface

    def wait_input(self):
        while True:
            text = self.interface.get_input_text()
            if not text:
                continue
            else:
                return text

    def take_command(self):
        if self.how_get_input == 0:
            res = self.recognize_offline()
        elif self.how_get_input == 1:
            res = self.recognize_online()
        elif self.how_get_input == 2:
            res = self.wait_input()
        print(res,'*')
        return res

    def play_sound_init(self):
        sound='../Sounds/lbpnotification.mp3'
        mixer.init()
        mixer.music.load(sound)
        mixer.music.play()

    def play_sound_end():
        sound='../Sounds/tethys.mp3'
        mixer.init()
        mixer.music.load(sound)
        mixer.music.play()

    def recognize_online(self):
        hear = sr.Recognizer()
        with sr.Microphone() as source:
            #print("Ouvindo...")
            self.play_sound_init()
            hear.pause_threshold = 1
            audio = hear.listen(source)
        try:
            #print('Aguarde...')
            self.play_sound_end()
            query = hear.recognize_google(audio,language="pt-BR")
        except Exception as e:
            #self.engine_vstt.speak('Não conseguir entender oque disse')
            print(e)
            return None
        return query.lower()
    
    def recognize_offline(self):
        hear=sr.Recognizer()
        with sr.Microphone() as source:
            #print("Ouvindo...")
            self.play_sound_init()
            hear.pause_threshold = 1
            audio = hear.listen(source)
        try:
            #print('Aguarde...')
            self.play_sound_end()
            query = hear.recognize_sphinx(audio,language='en-IN')
        except Exception as e:
            #self.engine_vstt.speak('Não conseguir entender oque disse')
            print(e)
            return None
        return query.lower()

    def speak(self,audio):
        self.interface.set_stack(audio)
        audio = '"'+audio+'"'
        x = popen(self.cmd+audio).read()

    def confirm(self):
        st = 'não'
        saida = ''
        while st != 'sim':
            saida = self.take_command()
            self.speak('Você disse '+saida+', está correto?')
            st = self.take_command()
            if st.find('sim')!=-1:
                break
        return saida