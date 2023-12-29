import speech_recognition as sr
from os import popen
from pygame import mixer
from Graphical_view import InterfaceView
#from pocketsphinx import LiveSpeech
#for phrase in LiveSpeech(): print(phrase)

class EngineVSTTView(InterfaceView):
    def __init__(self):
        super().__init__()
        self.cmd = 'spd-say -o "rhvoice" -w -t female1 '# spd-say -o "rhvoice" -w -y "Portuguese (Brazil)+Belinda"
        self.how_get_input = 2

    def wait_input(self):
        while True:
            text = self.get_input_text()
            if text:
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
        self.set_is_talking()
        audio = '"'+audio+'"'
        _ = popen(self.cmd+audio).read()
        self.set_is_talking()

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
