import pygame
import math
import random

class Colors:
    def __init__(self):
        self.WHITE =     (255, 255, 255)
        self.BLUE =      (  0,   0, 255)
        self.GREEN =     (  0, 255,   0)
        self.RED =       (255,   0,   0)

class Interface:
    def __init__(self):
        self.colors = Colors()
        self.screen = None    
        self.running = True
        self.typing = False
        self.input_text = ""
        self.gradient_color = [0,255,0]
        self.wave_color = [0,0,255]
        self.stack = []
        self.fps = 40

    def set_stack(self,text):
        text = text.split()
        stack = []
        period = int(self.fps*0.461538462)
        
        for word in text:
            word = [int(math.sin(ord(w))*100) for w in word]
            s_word = []
            for i in range(len(word)-1):
                if word[i] < word[i+1]:
                    s_word.extend([j for j in range(word[i],word[i+1],period)])
                else:
                    nword = [j for j in range(word[i+1],word[i],period)]
                    nword = nword[::-1]
                    s_word.extend(nword)
            stack.extend(s_word.copy())
        self.stack = stack[::-1]

    def get_pos_stack(self):
        if self.stack != []:
            return self.stack.pop()
        else:
            return 0

    def draw_waves(self,h):
        x = 168
        if h > 0:
            perc = 0.0833
            for i in range(6):
                pygame.draw.rect(self.screen, self.colors.BLUE,[x,350,34,h*perc])
                x += 39
                perc += 0.16667
            
            for i in range(6):
                pygame.draw.rect(self.screen, self.colors.BLUE,[x,350,34,h*perc])
                x += 39
                perc -= 0.16667
        elif h < 0:
            h *= -1
            perc = 1
            for i in range(6):
                pygame.draw.rect(self.screen, self.colors.BLUE,[x,350,34,h*perc])
                x += 39
                perc -= 0.16667

            pygame.draw.rect(self.screen, self.colors.BLUE,[x,350,34,h*0.05])

            for i in range(6):
                pygame.draw.rect(self.screen, self.colors.BLUE,[x,350,34,h*perc])
                x += 39
                perc += 0.16667
        else:
            self.get_gradient_color()


    def drawCircle(self):
        pos = (400,350)

        pygame.draw.circle(self.screen, self.gradient_color, pos, 250,width=10)
    
        PI = math.pi
        h = self.get_pos_stack()
        
        self.draw_waves(h)

    def get_input_text(self):
        if self.input_text:
            text = self.input_text
            self.input_text = ""
            return text
        else:
            return None

    def get_gradient_color(self):
        index = random.randint(0,2)
        index_wave = random.randint(1,2)
        if self.wave_color[index_wave]+1 > 255:
            self.wave_color[index_wave] = 50
        else:
            self.wave_color[index_wave] += 5

        if self.gradient_color[index]+1 > 255:
            self.gradient_color[index] = 0
        else:
            self.gradient_color[index] += 5

    def reset_gradient(self):
        self.wave_color = [0,255,0]

    def shutdown(self):
        self.running = False

    def start(self):
        (width, height) = (800, 720)
        background_color = (0,0,0)

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        
        icon = pygame.image.load("./icons/minerva_icon_final.png")
        pygame.display.set_icon(icon)

        clock = pygame.time.Clock()
        pygame.display.set_caption("MINERVA")

        font = pygame.font.SysFont(None, 95)

        text = ""
        while self.running:
            self.screen.fill(background_color)

            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.typing = True
                elif event.type == pygame.KEYDOWN and self.typing:
                    if event.key == pygame.K_RETURN:
                        self.typing = False
                        self.input_text = text
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text =  text[:-1]
                    else:
                        text += event.unicode

            if self.typing:
                rect = pygame.draw.rect(self.screen,self.colors.RED,[10,600,710,200],2)
                text_surf = font.render(text, True, self.colors.RED)
                self.screen.blit(text_surf, (10,600,710,200))
            self.drawCircle()

            pygame.display.update()
            clock.tick(self.fps)

inter = Interface()
inter.set_stack("bom dia mestre como vai?")
inter.start()