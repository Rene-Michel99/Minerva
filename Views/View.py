import pygame
import math
import random
import numpy as np

class Colors:
    def __init__(self):
        self.WHITE =     (255, 255, 255)
        self.BLUE =      (  0,   0, 255)
        self.GREEN =     (  0, 255,   0)
        self.RED =       (255,   0,   0)

class Interface:
    def __init__(self):
        self.RUNNING = True
        self.TYPING = False
        self.IS_TALKING = False
        self.INPUT_TEXT = ""

        self.colors = Colors()
        self.screen = None
        self.gradient_color = [0,0,255]
        self.wave_color = [0,0,255]
        self.stack = []
        self.fps = 40

    def get_waves(self):
        start_time = 0
        end_time = 1
        sample_rate = 476
        time = np.arange(start_time, end_time, 1/sample_rate)
        theta = random.randint(1,10)
        frequency = random.randint(1,10)
        amplitude = random.randint(1,100)
        waves = amplitude * np.sin(2 * np.pi * frequency * time + theta)
        return waves

    def set_is_talking(self):
        self.IS_TALKING = not self.IS_TALKING

    def draw_waves(self):
        x = 160
        waves = self.get_waves()
        
        for y in waves:
            pygame.draw.rect(self.screen, self.colors.GREEN,[x,y+350,5,10])
            x += 1

    def draw(self):
        pos = (400,350)
        pygame.draw.circle(self.screen, self.gradient_color, pos, 250,width=10)
    
        PI = math.pi

        if self.IS_TALKING:
            self.draw_waves()
        else:
            self.get_gradient_color()

    def get_input_text(self):
        if self.INPUT_TEXT:
            text = self.INPUT_TEXT
            self.INPUT_TEXT = ""
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
        self.RUNNING = False

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
        while self.RUNNING:
            self.screen.fill(background_color)

            ev = pygame.event.get()

            for event in ev:
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.TYPING = True
                elif event.type == pygame.KEYDOWN and self.TYPING:
                    if event.key == pygame.K_RETURN:
                        self.TYPING = False
                        self.INPUT_TEXT = text
                        text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text =  text[:-1]
                    else:
                        text += event.unicode

            if self.TYPING:
                rect = pygame.draw.rect(self.screen,self.colors.RED,[10,600,710,200],2)
                text_surf = font.render(text, True, self.colors.RED)
                self.screen.blit(text_surf, (10,600,710,200))
            self.draw()

            pygame.display.update()
            clock.tick(self.fps)

inter = Interface()
inter.set_is_talking()
inter.start()