class ColorWheel:
    def __init__(self):
        self.RED   = "\033[1;31m"  
        self.BLUE  = "\033[1;34m"
        self.CYAN  = "\033[1;36m"
        self.GREEN = "\033[0;32m"
        self.RESET = "\033[0;0m"
        self.BOLD    = "\033[;1m"
        self.REVERSE = "\033[;7m"


class View:
    def __init__(self):
        self.RUNNING = False
        self.IS_SPEAKING = False
        self.COLORWHEEL = ColorWheel()

        self.IDLE_FRAMES = open("animation/idle.txt","r",encoding='utf-8').read()
        self.IDLE_FRAMES = self.IDLE_FRAMES.split("0")

        self.SPEAKING_FRAMES = open("animation/speaking.txt","r",encoding='utf-8').read()
        self.SPEAKING_FRAMES = self.SPEAKING_FRAMES.split("0")

    def set_speaking(self):
        self.IS_SPEAKING = not self.IS_SPEAKING

    def pprint(self,text):
        print("",flush=True)
        print(f"{self.COLORWHEEL.BLUE}Ok")
        print(self.COLORWHEEL.RESET)

    def speaking(self):
        import time,os
        while self.IS_SPEAKING:
            for frame in self.SPEAKING_FRAMES:
                os.system("cls")
                print(self.COLORWHEEL.BLUE+frame)
                time.sleep(0.01)

    def idle(self):
        import time,os
        while True:
            for frame in self.IDLE_FRAMES:
                os.system("cls")
                print(self.COLORWHEEL.BLUE+frame)
                time.sleep(0.01)

    def start(self):
        self.RUNNING = True
        self.IS_SPEAKING = True
        while self.RUNNING:
            self.speaking()
            
view = View()
view.start()